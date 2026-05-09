#!/usr/bin/env python3
"""
WeChat Publisher MCP Server for DeerFlow FireSpot
==================================================
完整的微信公众号发布 MCP 服务器实现

功能：
- 真实的微信公众号API调用
- 图片素材上传（永久素材）
- Markdown转HTML
- 草稿创建和发布

Author: FireSpot Team
Version: 2.0.0 (Production)
"""

import asyncio
import json
import logging
import os
import base64
import mimetypes
from typing import Any, Dict, Optional
from datetime import datetime
from pathlib import Path

import httpx

# 微信公众号 API 配置
WECHAT_APPID = os.environ.get("WECHAT_APPID", "")
WECHAT_APPSECRET = os.environ.get("WECHAT_APPSECRET", "")

# API端点
WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin"
TOKEN_ENDPOINT = f"{WECHAT_API_BASE}/token"
UPLOAD_MATERIAL_ENDPOINT = f"{WECHAT_API_BASE}/material/add_material"
ADD_DRAFT_ENDPOINT = f"{WECHAT_API_BASE}/draft/add"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeChatPublisher:
    """微信公众号发布器（完整实现）"""

    def __init__(self):
        self.appid = WECHAT_APPID
        self.secret = WECHAT_APPSECRET
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[float] = None
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """获取或创建HTTP客户端"""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client

    async def close(self):
        """关闭HTTP客户端"""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get_access_token(self) -> str:
        """
        获取微信访问令牌（真实实现）

        Returns:
            str: access_token

        Raises:
            Exception: 获取失败时抛出异常
        """
        # 检查是否已有有效的token
        if self.access_token and self.token_expires_at:
            # 提前5分钟刷新token
            if datetime.now().timestamp() < self.token_expires_at - 300:
                logger.info("🔑 使用缓存的access_token")
                return self.access_token

        logger.info("🔑 获取新的access_token")

        if not self.appid or not self.secret:
            raise Exception("WECHAT_APPID 或 WECHAT_APPSECRET 环境变量未配置")

        try:
            client = await self._get_client()
            response = await client.get(
                TOKEN_ENDPOINT,
                params={
                    "grant_type": "client_credential",
                    "appid": self.appid,
                    "secret": self.secret
                }
            )
            response.raise_for_status()
            data = response.json()

            if "access_token" not in data:
                error_msg = data.get("errmsg", "未知错误")
                error_code = data.get("errcode", "N/A")
                raise Exception(f"获取access_token失败: errcode={error_code}, errmsg={error_msg}")

            self.access_token = data["access_token"]
            expires_in = data.get("expires_in", 7200)
            self.token_expires_at = datetime.now().timestamp() + expires_in

            logger.info(f"✅ 获取access_token成功: {self.access_token[:20]}...")
            return self.access_token

        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP错误: {e.response.status_code}, {e.response.text}")
        except Exception as e:
            logger.error(f"❌ 获取access_token失败: {e}")
            raise

    async def upload_image_material(
        self,
        image_path: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        上传图片素材到微信公众号

        Args:
            image_path: 图片文件路径
            max_retries: 最大重试次数

        Returns:
            dict: 包含media_id和URL的字典
        """
        if not os.path.exists(image_path):
            return {
                "ok": False,
                "error": f"图片文件不存在: {image_path}"
            }

        logger.info(f"📷 上传图片素材: {image_path}")

        for attempt in range(max_retries):
            try:
                access_token = await self.get_access_token()
                client = await self._get_client()

                # 读取图片文件
                with open(image_path, "rb") as f:
                    files = {
                        "media": (
                            os.path.basename(image_path),
                            f,
                            mimetypes.guess_type(image_path)[0] or "image/jpeg"
                        )
                    }

                    response = await client.post(
                        f"{UPLOAD_MATERIAL_ENDPOINT}?access_token={access_token}&type=image",
                        files=files
                    )

                response.raise_for_status()
                data = response.json()

                # 检查是否有错误码（成功的响应没有errcode字段）
                if "errcode" in data and data["errcode"] != 0:
                    error_msg = data.get("errmsg", "未知错误")
                    error_code = data.get("errcode")
                    # 输出完整的响应以便调试
                    logger.error(f"微信API响应: {data}")
                    if attempt < max_retries - 1:
                        logger.warning(f"⚠️ 上传失败，重试 {attempt + 1}/{max_retries}: {error_msg}")
                        await asyncio.sleep(1)
                        continue
                    raise Exception(f"上传图片失败: errcode={error_code}, errmsg={error_msg}")

                media_id = data.get("media_id")
                url = data.get("url")

                logger.info(f"✅ 图片上传成功: media_id={media_id}")

                return {
                    "ok": True,
                    "media_id": media_id,
                    "url": url
                }

            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️ 上传失败，重试 {attempt + 1}/{max_retries}: {e}")
                    await asyncio.sleep(1)
                    continue
                logger.error(f"❌ 上传图片失败: {e}")
                return {
                    "ok": False,
                    "error": str(e)
                }

    async def upload_image_from_base64(
        self,
        image_base64: str,
        filename: str = "image.jpg",
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        上传base64编码的图片到微信公众号

        Args:
            image_base64: base64编码的图片数据
            filename: 文件名
            max_retries: 最大重试次数

        Returns:
            dict: 包含media_id和URL的字典
        """
        logger.info(f"📷 上传base64图片素材: {filename}")

        try:
            # 解码base64
            image_data = base64.b64decode(image_base64)

            # 临时保存到文件
            temp_path = f"/tmp/wechat_upload_{datetime.now().timestamp()}_{filename}"
            with open(temp_path, "wb") as f:
                f.write(image_data)

            # 上传
            result = await self.upload_image_material(temp_path, max_retries)

            # 清理临时文件
            try:
                os.remove(temp_path)
            except:
                pass

            return result

        except Exception as e:
            logger.error(f"❌ 上传base64图片失败: {e}")
            return {
                "ok": False,
                "error": str(e)
            }

    async def create_draft(
        self,
        title: str,
        content: str,
        thumb_media_id: str,
        digest: str = "",
        author: str = "FireSpot AI",
        show_cover_pic: int = 1,
        need_open_comment: int = 1,
        only_fans_can_comment: int = 0,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        创建微信公众号草稿

        Args:
            title: 文章标题
            content: 文章内容（Markdown或HTML格式）
            thumb_media_id: 封面图片media_id
            digest: 摘要（可选，不提供会自动提取）
            author: 作者
            show_cover_pic: 是否显示封面图（0=不显示，1=显示）
            need_open_comment: 是否开启评论（0=不开启，1=开启）
            only_fans_can_comment: 是否只有粉丝可以评论（0=所有人，1=粉丝）
            max_retries: 最大重试次数

        Returns:
            dict: 包含media_id的字典
        """
        logger.info(f"📝 创建微信草稿: {title}")

        # 转换Markdown到HTML（如果是Markdown格式）
        html_content = self._markdown_to_html(content)

        # 如果没有提供摘要，从内容中提取
        if not digest:
            digest = self._extract_digest(html_content, max_length=120)

        # 构建请求体
        payload = {
            "articles": [
                {
                    "title": title,
                    "author": author,
                    "digest": digest,
                    "content": html_content,
                    "content_source_url": "",
                    "thumb_media_id": thumb_media_id,
                    "show_cover_pic": show_cover_pic,
                    "need_open_comment": need_open_comment,
                    "only_fans_can_comment": only_fans_can_comment
                }
            ]
        }

        for attempt in range(max_retries):
            try:
                access_token = await self.get_access_token()
                client = await self._get_client()

                response = await client.post(
                    f"{ADD_DRAFT_ENDPOINT}?access_token={access_token}",
                    json=payload
                )

                response.raise_for_status()
                data = response.json()

                # 检查是否有错误码（成功的响应没有errcode字段）
                if "errcode" in data and data["errcode"] != 0:
                    error_msg = data.get("errmsg", "未知错误")
                    error_code = data.get("errcode")

                    # Token过期，重新获取
                    if error_code in [40001, 42001]:
                        logger.info("🔄 Token过期，重新获取...")
                        self.access_token = None
                        self.token_expires_at = None
                        if attempt < max_retries - 1:
                            await asyncio.sleep(1)
                            continue

                    if attempt < max_retries - 1:
                        logger.warning(f"⚠️ 创建草稿失败，重试 {attempt + 1}/{max_retries}: {error_msg}")
                        await asyncio.sleep(1)
                        continue

                    raise Exception(f"创建草稿失败: errcode={error_code}, errmsg={error_msg}")

                media_id = data.get("media_id")

                logger.info(f"✅ 微信草稿创建成功: media_id={media_id}")

                return {
                    "ok": True,
                    "media_id": media_id,
                    "draft_id": media_id,
                    "created_at": datetime.now().isoformat(),
                    "title": title,
                    "digest": digest
                }

            except httpx.HTTPStatusError as e:
                error_text = e.response.text
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️ HTTP错误，重试 {attempt + 1}/{max_retries}: {error_text}")
                    await asyncio.sleep(1)
                    continue
                logger.error(f"❌ HTTP错误: {error_text}")
                return {
                    "ok": False,
                    "error": f"HTTP错误: {error_text}"
                }

            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️ 创建草稿失败，重试 {attempt + 1}/{max_retries}: {e}")
                    await asyncio.sleep(1)
                    continue
                logger.error(f"❌ 创建草稿失败: {e}")
                return {
                    "ok": False,
                    "error": str(e)
                }

    def _markdown_to_html(self, content: str) -> str:
        """
        将Markdown内容转换为HTML（微信格式）

        Args:
            content: Markdown内容

        Returns:
            str: HTML内容
        """
        try:
            import markdown
        except ImportError:
            logger.warning("⚠️ markdown库未安装，返回原内容")
            return content

        # 配置markdown扩展
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code'
        ]

        # 转换为HTML
        html = markdown.markdown(content, extensions=extensions)

        # 微信公众号需要特殊的section标签
        html_content = f'<section class="wx-editor">{html}</section>'

        return html_content

    def _extract_digest(self, html_content: str, max_length: int = 80) -> str:
        """
        从HTML内容中提取摘要（微信公众号要求纯文本，严格限制长度）

        Args:
            html_content: HTML内容
            max_length: 最大长度（默认80字符，微信digest字段限制120，但留余量更安全）

        Returns:
            str: 摘要文本
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # 优先获取第一段文字内容
            first_p = soup.find('p')
            if first_p:
                text = first_p.get_text()
            else:
                # 如果没有段落，获取前200字符的文本
                text = soup.get_text()[:200]

            # 清理：去除换行、多余空格、HTML实体
            import re
            text = re.sub(r'\s+', ' ', text)  # 多个空白字符替换为单个空格
            text = text.strip()

            # 截断（确保不超过max_length）
            if len(text) > max_length:
                text = text[:max_length].rstrip() + "..."

            return text

        except ImportError:
            # 如果没有bs4，使用简单方法
            import re
            # 移除HTML标签
            text = re.sub(r'<[^>]+>', '', html_content)
            # 清理空白字符
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()

            # 截断
            if len(text) > max_length:
                text = text[:max_length].rstrip() + "..."

            return text


# ============================================================================
# MCP Server 实现
# ============================================================================

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent

    wechat_server = Server("wechat-publisher-server")
    publisher = WeChatPublisher()

    @wechat_server.list_tools()
    async def list_wechat_tools() -> list[Tool]:
        return [
            Tool(
                name="wechat_get_access_token",
                description="获取微信公众号access_token",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="wechat_upload_image",
                description="上传本地图片文件到微信公众号素材库",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "图片文件路径（绝对路径或相对于/mnt/user-data的路径）"
                        }
                    },
                    "required": ["image_path"]
                }
            ),
            Tool(
                name="wechat_upload_image_base64",
                description="上传base64编码的图片到微信公众号素材库",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "image_base64": {
                            "type": "string",
                            "description": "base64编码的图片数据"
                        },
                        "filename": {
                            "type": "string",
                            "description": "文件名（可选，默认为image.jpg）"
                        }
                    },
                    "required": ["image_base64"]
                }
            ),
            Tool(
                name="wechat_create_draft",
                description="创建微信公众号草稿文章",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "文章标题"
                        },
                        "content": {
                            "type": "string",
                            "description": "文章内容（支持Markdown或HTML格式）"
                        },
                        "thumb_media_id": {
                            "type": "string",
                            "description": "封面图片的media_id（需先调用wechat_upload_image获取）"
                        },
                        "digest": {
                            "type": "string",
                            "description": "文章摘要（可选，不提供会自动从内容提取）"
                        },
                        "author": {
                            "type": "string",
                            "description": "作者名称（可选，默认为FireSpot AI）"
                        },
                        "show_cover_pic": {
                            "type": "integer",
                            "description": "是否显示封面图（0=不显示，1=显示，默认1）"
                        },
                        "need_open_comment": {
                            "type": "integer",
                            "description": "是否开启评论（0=不开启，1=开启，默认1）"
                        }
                    },
                    "required": ["title", "content", "thumb_media_id"]
                }
            ),
            Tool(
                name="wechat_publish_full_workflow",
                description="完整的工作流：上传图片并创建草稿（一步完成）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "文章标题"
                        },
                        "content": {
                            "type": "string",
                            "description": "文章内容（支持Markdown或HTML格式）"
                        },
                        "cover_image_path": {
                            "type": "string",
                            "description": "封面图片路径"
                        },
                        "digest": {
                            "type": "string",
                            "description": "文章摘要（可选）"
                        },
                        "author": {
                            "type": "string",
                            "description": "作者名称（可选）"
                        }
                    },
                    "required": ["title", "content", "cover_image_path"]
                }
            )
        ]

    @wechat_server.call_tool()
    async def call_wechat_tool(name: str, arguments: Any) -> list[TextContent]:
        try:
            if name == "wechat_get_access_token":
                result = await publisher.get_access_token()
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "ok": True,
                        "access_token": result,
                        "expires_at": publisher.token_expires_at
                    }, ensure_ascii=False)
                )]

            elif name == "wechat_upload_image":
                image_path = arguments.get("image_path")
                # 处理虚拟路径
                if image_path.startswith("/mnt/user-data/"):
                    # 转换虚拟路径到实际路径
                    from pathlib import Path
                    # 假设当前目录是backend
                    actual_path = Path.cwd() / ".deer-flow" / image_path.replace("/mnt/", "")
                    image_path = str(actual_path)

                result = await publisher.upload_image_material(image_path)
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

            elif name == "wechat_upload_image_base64":
                image_base64 = arguments.get("image_base64")
                filename = arguments.get("filename", "image.jpg")
                result = await publisher.upload_image_from_base64(image_base64, filename)
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

            elif name == "wechat_create_draft":
                title = arguments.get("title")
                content = arguments.get("content")
                thumb_media_id = arguments.get("thumb_media_id")
                digest = arguments.get("digest", "")
                author = arguments.get("author", "FireSpot AI")
                show_cover_pic = arguments.get("show_cover_pic", 1)
                need_open_comment = arguments.get("need_open_comment", 1)

                result = await publisher.create_draft(
                    title=title,
                    content=content,
                    thumb_media_id=thumb_media_id,
                    digest=digest,
                    author=author,
                    show_cover_pic=show_cover_pic,
                    need_open_comment=need_open_comment
                )
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

            elif name == "wechat_publish_full_workflow":
                title = arguments.get("title")
                content = arguments.get("content")
                cover_image_path = arguments.get("cover_image_path")
                digest = arguments.get("digest", "")
                author = arguments.get("author", "FireSpot AI")

                # 处理虚拟路径
                if cover_image_path.startswith("/mnt/user-data/"):
                    from pathlib import Path
                    actual_path = Path.cwd() / ".deer-flow" / cover_image_path.replace("/mnt/", "")
                    cover_image_path = str(actual_path)

                # Step 1: 上传封面图
                logger.info("📋 开始完整发布流程...")
                upload_result = await publisher.upload_image_material(cover_image_path)

                if not upload_result.get("ok"):
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "ok": False,
                            "error": f"封面图上传失败: {upload_result.get('error')}",
                            "step": "upload_image"
                        }, ensure_ascii=False)
                    )]

                # Step 2: 创建草稿
                draft_result = await publisher.create_draft(
                    title=title,
                    content=content,
                    thumb_media_id=upload_result["media_id"],
                    digest=digest,
                    author=author
                )

                return [TextContent(type="text", text=json.dumps(draft_result, ensure_ascii=False))]

            else:
                return [TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name}"}, ensure_ascii=False)
                )]

        except Exception as e:
            logger.exception(f"❌ 工具调用失败: {name}")
            return [TextContent(
                type="text",
                text=json.dumps({
                    "ok": False,
                    "error": str(e),
                    "tool": name
                }, ensure_ascii=False)
            )]

    async def main_wechat():
        """启动微信发布 MCP 服务器"""
        async with stdio_server() as (read_stream, write_stream):
            await wechat_server.run(
                read_stream,
                write_stream,
                wechat_server.create_initialization_options()
            )

    if __name__ == "__main__":
        asyncio.run(main_wechat())

except ImportError as e:
    logger.error(f"❌ MCP SDK 未安装: {e}")
    logger.info("💡 请安装: pip install mcp")
    logger.info("💡 或者: uv add mcp")
