#!/usr/bin/env python3
import argparse
import base64
import http.client
import json
import mimetypes
import os
import re
import sys
import time
import uuid
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


DATA_URL_RE = re.compile(r"^data:(?P<mime>[^;]+);base64,(?P<data>.+)$", re.IGNORECASE)
PRIVATE_CONFIG_PATH = Path.home() / ".codex" / "image-generation.json"
DEFAULT_REQUEST_TIMEOUT = 900
DEFAULT_RETRY_COUNT = 3
CONFIG_HELP = """首次使用前需要配置图片接口凭据。任选一种方式：
1. 创建私有配置文件 ~/.codex/image-generation.json：
   mkdir -p ~/.codex
   文件内容示例：
   {"base_url": "https://你的图片接口域名/v1", "api_key": "你的 API Key"}
2. 或在当前终端临时设置环境变量：
   export IMAGE_BASE_URL="https://你的图片接口域名/v1"
   export IMAGE_API_KEY="你的 API Key"
也兼容 OPENAI_BASE_URL / OPENAI_API_KEY。
不要把真实 Key 写进 skill 文件、仓库、压缩包或聊天记录。"""


def fail(message: str, status_code: int = 1):
    print(json.dumps({"ok": False, "error": message}, ensure_ascii=False))
    sys.exit(status_code)


def is_retryable_disconnect(exc: Exception):
    return isinstance(exc, http.client.RemoteDisconnected)


def request_with_retry(req: urllib.request.Request, retry_count: int):
    attempts = retry_count + 1
    last_exc = None

    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(req, timeout=DEFAULT_REQUEST_TIMEOUT) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            try:
                raw = exc.read().decode("utf-8")
                data = json.loads(raw)
                message = data.get("error", {}).get("message") or data.get("message") or raw
            except Exception:
                message = exc.reason or f"HTTP {exc.code}"
            fail(f"接口调用失败: {message}")
        except urllib.error.URLError as exc:
            reason = exc.reason
            if is_retryable_disconnect(reason) and attempt < attempts:
                last_exc = reason
                time.sleep(min(attempt, 3))
                continue
            fail(f"网络请求失败: {reason}")
        except http.client.RemoteDisconnected as exc:
            if attempt < attempts:
                last_exc = exc
                time.sleep(min(attempt, 3))
                continue
            fail(f"网络请求失败: {exc}")

    if last_exc is not None:
        fail(f"网络请求失败: {last_exc}")
    fail("网络请求失败: 未知错误")


def load_private_config():
    if not PRIVATE_CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(PRIVATE_CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"读取私有配置失败: {exc}")


def load_runtime_settings(args):
    config = load_private_config()
    base_url = (
        args.base_url
        or os.environ.get("IMAGE_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or config.get("base_url")
    )
    api_key = (
        args.api_key
        or os.environ.get("IMAGE_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or config.get("api_key")
    )
    missing = []
    if not base_url:
        missing.append("base_url")
    if not api_key:
        missing.append("api_key")
    if missing:
        fail(f"缺少 {', '.join(missing)}。\n{CONFIG_HELP}")
    return str(base_url).rstrip("/"), str(api_key)


def build_api_url(base_url: str, mode: str):
    endpoint = "/images/generations" if mode == "generate" else "/images/edits"
    if base_url.endswith("/v1"):
        return f"{base_url}{endpoint}"
    return f"{base_url}/v1{endpoint}"


def guess_mime(path: Path):
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def guess_mime_from_url(url: str):
    mime, _ = mimetypes.guess_type(url)
    return mime or "application/octet-stream"


def download_image(url: str):
    try:
        with urllib.request.urlopen(url, timeout=120) as response:
            content_type = response.headers.get_content_type() or guess_mime_from_url(url)
            data = response.read()
    except urllib.error.HTTPError as exc:
        fail(f"下载图片失败: HTTP {exc.code}")
    except urllib.error.URLError as exc:
        fail(f"下载图片失败: {exc.reason}")

    if not data:
        fail("下载图片失败: 返回内容为空")
    return Path(url.split("?")[0]).name or "image", content_type, data


def load_image_part(value: str, fallback_name: str):
    if value.startswith(("http://", "https://")):
        filename, mime, data = download_image(value)
        if "." not in filename:
            filename = f"{fallback_name}.{choose_extension(None, mime)}"
        return filename, mime, data
    if value.startswith("data:"):
        mime, data = parse_data_url(value)
        ext = choose_extension(None, mime)
        return f"{fallback_name}.{ext}", mime, data

    path = Path(value).expanduser()
    if not path.exists():
        fail(f"图片文件不存在: {value}")
    return path.name, guess_mime(path), path.read_bytes()


def parse_data_url(data_url: str):
    match = DATA_URL_RE.match(data_url)
    if not match:
        fail("返回的 data URL 格式无效")
    try:
        data = base64.b64decode(match.group("data"))
    except Exception as exc:
        fail(f"解析返回图片失败: {exc}")
    return match.group("mime"), data


def choose_extension(output_format: str | None, mime: str | None = None):
    if output_format:
        normalized = output_format.lower()
        return "jpg" if normalized == "jpeg" else normalized
    if mime:
        ext = mimetypes.guess_extension(mime)
        if ext:
            return ext.lstrip(".").replace("jpe", "jpg")
    return "png"


def ensure_output_dir():
    output_dir = Path.cwd() / "image"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def resolve_output_dir(value: str | None):
    if not value:
        return ensure_output_dir()
    output_dir = Path(value).expanduser()
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def save_images(image_entries, output_format: str | None, output_dir: Path):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    paths = []

    for index, item in enumerate(image_entries, start=1):
        ext = choose_extension(output_format)
        if item.get("b64_json"):
            try:
                binary = base64.b64decode(item["b64_json"])
            except Exception as exc:
                fail(f"解码返回图片失败: {exc}")
        elif item.get("url", "").startswith("data:"):
            mime, binary = parse_data_url(item["url"])
            ext = choose_extension(output_format, mime)
        else:
            fail("接口返回中未找到可保存的图片数据")

        file_path = output_dir / f"{timestamp}-{index:02d}.{ext}"
        file_path.write_bytes(binary)
        paths.append(str(file_path))

    return paths


def post_json(url: str, api_key: str, payload: dict):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    return request_with_retry(req, DEFAULT_RETRY_COUNT)


def post_multipart(url: str, api_key: str, fields: dict, files: list[tuple[str, str, str, bytes]]):
    boundary = f"----image-generation-{uuid.uuid4().hex}"
    chunks = []

    for name, value in fields.items():
        if value is None:
            continue
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )

    for field_name, filename, mime, data in files:
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    f'Content-Disposition: form-data; name="{field_name}"; '
                    f'filename="{filename}"\r\n'
                ).encode("utf-8"),
                f"Content-Type: {mime}\r\n\r\n".encode("utf-8"),
                data,
                b"\r\n",
            ]
        )

    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(chunks)
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Authorization": f"Bearer {api_key}",
        },
    )
    return request_with_retry(req, DEFAULT_RETRY_COUNT)


def add_optional_fields(payload: dict, args, fields: list[str]):
    for field in fields:
        value = getattr(args, field, None)
        if value is not None:
            payload[field] = value


def build_generation_payload(args):
    if not args.prompt:
        fail("缺少 prompt")

    payload = {
        "model": args.model or "gpt-image-2",
        "prompt": args.prompt,
        "response_format": "b64_json",
        "stream": False,
        "n": args.n or 1,
    }
    add_optional_fields(
        payload,
        args,
        ["size", "quality", "background", "output_format", "output_compression", "partial_images", "moderation"],
    )
    return payload


def build_edit_payload(args):
    if not args.prompt:
        fail("缺少 prompt")
    if not args.image:
        fail("缺少要编辑的图片来源")

    payload = {
        "model": args.model or "gpt-image-2",
        "prompt": args.prompt,
        "response_format": "b64_json",
        "stream": False,
        "n": args.n or 1,
    }
    add_optional_fields(
        payload,
        args,
        [
            "size",
            "quality",
            "background",
            "output_format",
            "output_compression",
            "partial_images",
            "moderation",
            "input_fidelity",
        ],
    )
    return payload


def build_edit_files(args):
    files = []
    image_name, image_mime, image_data = load_image_part(args.image, "image")
    files.append(("image", image_name, image_mime, image_data))
    if args.mask:
        mask_name, mask_mime, mask_data = load_image_part(args.mask, "mask")
        files.append(("mask", mask_name, mask_mime, mask_data))
    return files


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["generate", "edit"], required=True)
    parser.add_argument("--prompt")
    parser.add_argument("--model")
    parser.add_argument("--image")
    parser.add_argument("--mask")
    parser.add_argument("--size")
    parser.add_argument("--quality")
    parser.add_argument("--background")
    parser.add_argument("--output-format", dest="output_format")
    parser.add_argument("--output-compression", dest="output_compression", type=int)
    parser.add_argument("--partial-images", dest="partial_images", type=int)
    parser.add_argument("--n", type=int)
    parser.add_argument("--moderation")
    parser.add_argument("--input-fidelity", dest="input_fidelity")
    parser.add_argument("--base-url", dest="base_url")
    parser.add_argument("--api-key", dest="api_key")
    parser.add_argument("--output-dir", dest="output_dir")
    return parser.parse_args()


def main():
    args = parse_args()
    base_url, api_key = load_runtime_settings(args)
    payload = build_generation_payload(args) if args.mode == "generate" else build_edit_payload(args)
    url = build_api_url(base_url, args.mode)
    if args.mode == "generate":
        response = post_json(url, api_key, payload)
    else:
        response = post_multipart(url, api_key, payload, build_edit_files(args))
    data = response.get("data")
    if not isinstance(data, list) or not data:
        fail("接口返回中缺少 data")

    used_params = {
        "model": payload.get("model", "gpt-image-2"),
        "size": payload.get("size"),
        "quality": payload.get("quality"),
        "background": payload.get("background"),
        "output_format": payload.get("output_format") or "png",
        "n": payload.get("n", 1),
    }
    if args.mode == "edit" and payload.get("input_fidelity") is not None:
        used_params["input_fidelity"] = payload.get("input_fidelity")

    paths = save_images(data, payload.get("output_format"), resolve_output_dir(args.output_dir))
    print(json.dumps({"ok": True, "paths": paths, "used_params": used_params}, ensure_ascii=False))


if __name__ == "__main__":
    main()
