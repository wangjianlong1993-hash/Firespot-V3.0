#!/usr/bin/env python3
"""
ZhiPuArts MCP Server for DeerFlow
===================================
智谱 AI GLM-Image 图片生成服务 - 为 FireSpot 提供专业科技风格图片生成能力
"""

import asyncio
import json
import logging
import os
import base64
from typing import Any, Dict, Optional
from datetime import datetime
from pathlib import Path

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    Server = None
    stdio_server = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ZhiPuArts API 配置
ZHIPUARTS_API_KEY = os.environ.get("ZHIPUARTS_API_KEY", "")
ZHIPUARTS_ENDPOINT = "https://open.bigmodel.cn/api/paas/v4/images/generations"
ZHIPUARTS_MODEL = "glm-image"  # GLM-Image 模型

# 图片输出目录
IMAGE_OUTPUT_BASE = os.environ.get("ZHIPUARTS_IMAGE_OUTPUT_DIR", "/tmp/zhipuarts_images")


class ZhiPuArtsImageGenerator:
    """ZhiPuArts 图片生成器"""

    def __init__(self):
        self.api_key = ZHIPUARTS_API_KEY
        self.model = ZHIPUARTS_MODEL
        self.output_dir = Path(IMAGE_OUTPUT_BASE)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_image_with_zhipuarts(
        self,
        prompt: str,
        size: str = "1280x1280",
        save_path: str = None
    ) -> Dict[str, Any]:
        """
        使用 ZhiPuArts API 生成图片

        Args:
            prompt: 图片生成提示词
            size: 图片尺寸，格式为 "宽x高"，如 "1280x1280"
            save_path: 保存路径（可选）

        Returns:
            包含图片路径和元数据的字典
        """
        try:
            logger.info(f"🎨 ZhiPuArts 生成图片: {prompt[:100]}...")

            # 如果有 API key，调用真实 API
            if self.api_key and self.api_key != "":
                return await self._call_zhipuarts_api(prompt, size, save_path)
            else:
                # 没有 API key，使用模拟生成（用于测试）
                logger.warning("⚠️ ZHIPUARTS_API_KEY 未设置，使用模拟生成")
                return await self._generate_mock_image(prompt, size, save_path)

        except Exception as e:
            logger.error(f"❌ 图片生成失败: {e}")
            return {
                "ok": False,
                "error": str(e)
            }

    async def _call_zhipuarts_api(
        self,
        prompt: str,
        size: str,
        save_path: str = None
    ) -> Dict[str, Any]:
        """调用真实的 ZhiPuArts API"""
        import httpx

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "prompt": prompt,
            "size": size
        }

        logger.info(f"📡 调用 ZhiPuArts API: {ZHIPUARTS_ENDPOINT}")
        logger.info(f"📝 参数: model={self.model}, size={size}")

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                ZHIPUARTS_ENDPOINT,
                headers=headers,
                json=payload
            )

            logger.info(f"📊 API 响应状态码: {response.status_code}")

            if response.status_code != 200:
                error_text = response.text
                logger.error(f"❌ API 调用失败: {error_text}")
                return {
                    "ok": False,
                    "error": f"API returned {response.status_code}: {error_text}"
                }

            result = response.json()

            # 解析响应
            if result.get("error"):
                error_msg = result.get("error", {}).get("message", "Unknown error")
                logger.error(f"❌ API 返回错误: {error_msg}")
                return {
                    "ok": False,
                    "error": error_msg
                }

            # 获取图片数据
            # ZhiPuArts API 返回格式可能有多种，需要根据实际文档调整
            image_data = None

            # 方式1: 直接返回 base64 数据
            if "data" in result and len(result["data"]) > 0:
                image_data = result["data"][0].get("b64_json")

            # 方式2: 返回图片 URL
            if not image_data and "data" in result and len(result["data"]) > 0:
                image_url = result["data"][0].get("url")
                if image_url:
                    # 下载图片
                    logger.info(f"📥 下载图片: {image_url}")
                    img_response = await client.get(image_url)
                    if img_response.status_code == 200:
                        image_data = base64.b64encode(img_response.content).decode('utf-8')

            if image_data:
                # 保存图片
                timestamp = datetime.now().timestamp()
                filename = save_path or f"zhipuarts_{int(timestamp)}.png"

                # 确保是绝对路径
                if not os.path.isabs(filename):
                    filename = str(self.output_dir / filename)

                # 解码 base64 并保存
                image_bytes = base64.b64decode(image_data)
                Path(filename).parent.mkdir(parents=True, exist_ok=True)
                with open(filename, "wb") as f:
                    f.write(image_bytes)

                logger.info(f"✅ 图片已保存: {filename}")

                return {
                    "ok": True,
                    "image_path": filename,
                    "image_url": f"file://{filename}",
                    "prompt": prompt,
                    "size": size,
                    "provider": "zhipuarts"
                }
            else:
                return {
                    "ok": False,
                    "error": "No image data in response"
                }

    async def _generate_mock_image(
        self,
        prompt: str,
        size: str,
        save_path: str = None
    ) -> Dict[str, Any]:
        """
        生成模拟图片（用于测试）

        创建最小的 PNG 文件作为占位图
        """
        try:
            timestamp = datetime.now().timestamp()
            filename = save_path or f"zhipuarts_mock_{int(timestamp)}.png"

            # 确保是绝对路径
            if not os.path.isabs(filename):
                filename = str(self.output_dir / filename)

            Path(filename).parent.mkdir(parents=True, exist_ok=True)

            # 解析尺寸
            try:
                width, height = map(int, size.split("x"))
            except:
                width, height = 1024, 1024

            # 创建最小的 PNG
            self._create_minimal_png(filename, width, height)
            logger.info(f"✅ 模拟图片已生成: {filename}")

            return {
                "ok": True,
                "image_path": filename,
                "image_url": f"file://{filename}",
                "prompt": prompt,
                "size": size,
                "provider": "zhipuarts",
                "mock": True
            }

        except Exception as e:
            logger.error(f"❌ 模拟图片生成失败: {e}")
            return {
                "ok": False,
                "error": str(e)
            }

    def _create_minimal_png(self, filename: str, width: int, height: int):
        """创建最小的 PNG 文件"""
        import struct

        # 创建一个简单的 PNG 文件
        with open(filename, "wb") as f:
            # PNG signature
            f.write(b'\x89PNG\r\n\x1a\n')

            # IHDR chunk
            ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
            f.write(struct.pack(">I", 13))  # length
            f.write(b"IHDR")
            f.write(ihdr)
            f.write(struct.pack(">I", 0x2144df1b))  # CRC

            # IDAT chunk (minimal)
            f.write(struct.pack(">I", 11))  # length
            f.write(b"IDAT")
            f.write(b'\x78\x9c\x62\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4')
            f.write(struct.pack(">I", 0x894b5ea5))  # CRC

            # IEND chunk
            f.write(struct.pack(">I", 0))
            f.write(b"IEND")
            f.write(struct.pack(">I", 0xae426082))  # CRC


# MCP Server 实现
if Server is not None:
    server = Server("zhipuarts-server")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="mcp_zhipuarts_generate_image",
                description="使用智谱 AI GLM-Image 生成专业科技风格图片（为 FireSpot 微信公众号内容服务）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "图片生成提示词（中文或英文）"
                        },
                        "size": {
                            "type": "string",
                            "description": "图片尺寸，格式为 '宽x高'，如 '1280x1280'、'1920x1080' 等",
                            "default": "1280x1280"
                        },
                        "save_path": {
                            "type": "string",
                            "description": "保存路径（可选，默认使用时间戳命名）"
                        }
                    },
                    "required": ["prompt"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        generator = ZhiPuArtsImageGenerator()

        if name == "mcp_zhipuarts_generate_image":
            result = await generator.generate_image_with_zhipuarts(
                prompt=arguments["prompt"],
                size=arguments.get("size", "1280x1280"),
                save_path=arguments.get("save_path")
            )
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

        else:
            return [TextContent(type="text", text=json.dumps({
                "ok": False,
                "error": f"Unknown tool: {name}"
            }, ensure_ascii=False, indent=2))]


async def main():
    """启动 MCP 服务器"""
    if Server is None:
        logger.warning("⚠️ MCP SDK 未安装，运行简化模式")
        logger.info("请安装: pip install mcp")
        return

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
