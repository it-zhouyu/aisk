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
    """获取当前模型的 API Key

    Returns:
        str | None: API Key，如果未配置则返回 None
    """
    model_config = get_current_model_config()
    if model_config:
        return model_config.get("api_key")
    return None


def get_base_url() -> str:
    """获取当前模型的 Base URL

    Returns:
        str: Base URL，如果未配置则返回默认值
    """
    model_config = get_current_model_config()
    if model_config:
        return model_config.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    return "https://dashscope.aliyuncs.com/compatible-mode/v1"


def get_model_name() -> str:
    """获取当前模型名称

    Returns:
        str: 模型名称，如果未配置则返回默认值
    """
    model_config = get_current_model_config()
    if model_config:
        return model_config.get("model_name", "qwen3-max")
    return "qwen3-max"


def get_current_model_config() -> dict | None:
    """获取当前激活的模型配置

    Returns:
        dict | None: 当前模型配置，如果未配置则返回 None
    """
    config = load_config()
    current = config.get("current_model", "")
    models = config.get("models", [])

    for model in models:
        if model.get("name") == current:
            return model

    # 如果没有找到当前模型，返回第一个模型
    if models:
        return models[0]

    return None


def get_all_models() -> list:
    """获取所有已保存的模型配置

    Returns:
        list: 模型配置列表
    """
    config = load_config()
    return config.get("models", [])


def set_current_model(model_name: str) -> bool:
    """设置当前激活的模型

    Args:
        model_name: 要激活的模型名称

    Returns:
        bool: 是否设置成功
    """
    config = load_config()
    models = config.get("models", [])
    model_names = [m.get("name") for m in models]

    if model_name not in model_names:
        return False

    config["current_model"] = model_name
    save_config(config)
    return True
