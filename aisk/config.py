"""配置文件管理模块"""
import json
from pathlib import Path


def get_config_path() -> Path:
    """获取配置文件路径"""
    return Path.home() / ".aisk" / "config.json"


def get_config_dir() -> Path:
    """获取配置目录路径"""
    return Path.home() / ".aisk"


def ensure_config_dir() -> None:
    """确保配置目录存在"""
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """加载配置文件

    Returns:
        dict: 配置字典，如果文件不存在则返回空字典
    """
    config_path = get_config_path()
    if not config_path.exists():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_config(config: dict) -> None:
    """保存配置到文件

    Args:
        config: 配置字典
    """
    ensure_config_dir()
    config_path = get_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_api_key() -> str | None:
    """获取 API Key

    Returns:
        str | None: API Key，如果未配置则返回 None
    """
    config = load_config()
    return config.get("api_key")


def get_base_url() -> str:
    """获取 Base URL

    Returns:
        str: Base URL，如果未配置则返回默认值
    """
    config = load_config()
    return config.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1")


def get_model_name() -> str:
    """获取模型名称

    Returns:
        str: 模型名称，如果未配置则返回默认值
    """
    config = load_config()
    return config.get("model_name", "qwen-max")
