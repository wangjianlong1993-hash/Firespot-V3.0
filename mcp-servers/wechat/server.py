"""
Firespot — 微信公众号 MCP 发布服务器
运行方式：python server.py
监听端口：3101
DeerFlow 通过 SSE 连接此服务，调用微信发布工具
"""

import os
import time
import json
import asyncio
import httpx
from typing import Optional
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent
from starlette.applications import Starlette
from starlette.routing import Route

# ── 配置（从环境变量读取）──────────────────────────────────────
WECHAT_APPID = os.environ["WECHAT_APPID"]
WECHAT_APPSECRET = os.environ["WECHAT_APPSECRET"]
API_BASE = "https://api.weixin.qq.com/cgi-bin"

# ── Token 缓存（内存，生产环境建议用 Redis）──────────────────
_token_cache: dict = {"token": None, "expires_at": 0}

async def get_access_token() -> str:
    """获取或刷新 access_token，提前 5 分钟刷新"""
    if _token_cache["token"] and time.time() < _token_cache["expires_at"] - 300:
        return _token_cache["token"]
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/token", params={
            "grant_type": "client_credential",
            "appid": WECHAT_APPID,
            "secret": WECHAT_APPSECRET
        })
        data = resp.json()
        if "errcode" in data:
            raise RuntimeError(f"获取 token 失败: {data}")
        _token_cache["token"] = data["access_token"]
        _token_cache["expires_at"] = time.time() + data["expires_in"]
    
    return _token_cache["token"]


# ── MCP 服务器定义 ────────────────────────────────────────────
server = Server("wechat-publisher")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="mcp_wechat_upload_media",
            description="上传图片到微信公众号素材库，返回 media_id",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_url": {"type": "string", "description": "图片的网络 URL（jpg/png，≤5MB）"},
                    "image_base64": {"type": "string", "description": "图片的 Base64 编码（与 image_url 二选一）"}
                }
            }
        ),
        Tool(
            name="mcp_wechat_create_draft",
            description="创建微信公众号图文草稿",
            inputSchema={
                "type": "object",
                "required": ["title", "thumb_media_id", "content"],
                "properties": {
                    "title": {"type": "string"},
                    "thumb_media_id": {"type": "string", "description": "封面图 media_id（由 upload_media 获取）"},
                    "content": {"type": "string", "description": "HTML 格式正文"},
                    "digest": {"type": "string", "description": "摘要，≤120字"},
                    "need_open_comment": {"type": "integer", "default": 1}
                }
            }
        ),
        Tool(
            name="mcp_wechat_publish",
            description="发布或定时发布微信公众号草稿",
            inputSchema={
                "type": "object",
                "required": ["media_id"],
                "properties": {
                    "media_id": {"type": "string", "description": "草稿 media_id"},
                    "schedule_time": {"type": "integer", "description": "定时发布时间戳（Unix秒），0=立即发布", "default": 0}
                }
            }
        ),
        Tool(
            name="mcp_wechat_get_status",
            description="查询微信公众号发布状态",
            inputSchema={
                "type": "object",
                "required": ["publish_id"],
                "properties": {
                    "publish_id": {"type": "string"}
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    token = await get_access_token()
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        if name == "mcp_wechat_upload_media":
            # 从 URL 下载图片后上传
            if "image_url" in arguments:
                img_resp = await client.get(arguments["image_url"])
                image_data = img_resp.content
                content_type = img_resp.headers.get("content-type", "image/jpeg")
            else:
                import base64
                image_data = base64.b64decode(arguments["image_base64"])
                content_type = "image/jpeg"
            
            resp = await client.post(
                f"{API_BASE}/media/upload",
                params={"access_token": token, "type": "image"},
                files={"media": ("cover.jpg", image_data, content_type)}
            )
            data = resp.json()
            if "errcode" in data and data["errcode"] != 0:
                return [TextContent(type="text", text=json.dumps({"error": data}))]
            return [TextContent(type="text", text=json.dumps({
                "media_id": data["media_id"],
                "url": data.get("url", "")
            }))]
        
        elif name == "mcp_wechat_create_draft":
            payload = {
                "articles": [{
                    "title": arguments["title"],
                    "thumb_media_id": arguments["thumb_media_id"],
                    "content": arguments["content"],
                    "digest": arguments.get("digest", ""),
                    "need_open_comment": arguments.get("need_open_comment", 1),
                    "content_source_url": ""
                }]
            }
            resp = await client.post(
                f"{API_BASE}/draft/add",
                params={"access_token": token},
                json=payload
            )
            data = resp.json()
            return [TextContent(type="text", text=json.dumps(data))]
        
        elif name == "mcp_wechat_publish":
            media_id = arguments["media_id"]
            schedule_time = arguments.get("schedule_time", 0)
            
            if schedule_time and schedule_time > 0:
                # 定时发布
                resp = await client.post(
                    f"{API_BASE}/freepublish/submit",
                    params={"access_token": token},
                    json={"media_id": media_id}
                )
            else:
                resp = await client.post(
                    f"{API_BASE}/freepublish/submit",
                    params={"access_token": token},
                    json={"media_id": media_id}
                )
            data = resp.json()
            return [TextContent(type="text", text=json.dumps(data))]
        
        elif name == "mcp_wechat_get_status":
            resp = await client.get(
                f"{API_BASE}/freepublish/get",
                params={"access_token": token, "publish_id": arguments["publish_id"]}
            )
            data = resp.json()
            return [TextContent(type="text", text=json.dumps(data))]
    
    return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


# ── SSE 传输层（DeerFlow 兼容）────────────────────────────────
sse = SseServerTransport("/messages/")

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())

async def handle_messages(request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

app = Starlette(routes=[
    Route("/sse", endpoint=handle_sse),
    Route("/messages/", endpoint=handle_messages, methods=["POST"]),
])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3101)
