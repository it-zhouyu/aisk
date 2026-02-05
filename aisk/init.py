"""初始化配置模块"""
import sys
from .config import save_config, load_config, get_config_path


DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL_NAME = "qwen-max"


def init_config() -> None:
    """交互式初始化配置"""
    print("🔧 aisk 配置初始化")
    print("=" * 40)

    # 加载现有配置（如果有）
    existing_config = load_config()

    # 获取 API Key
    if existing_config.get("api_key"):
        default_api_key = existing_config["api_key"]
        print(f"\n当前 API Key: {default_api_key[:8]}...{default_api_key[-4:]}")
        api_key_input = input(f"请输入 API Key (直接回车保留当前值): ").strip()
        if not api_key_input:
            api_key = default_api_key
        else:
            api_key = api_key_input
    else:
        while True:
            api_key = input("\n请输入 API Key (必填): ").strip()
            if api_key:
                break
            print("❌ API Key 不能为空，请重新输入。")

    # 获取 Base URL
    current_base_url = existing_config.get("base_url", DEFAULT_BASE_URL)
    print(f"\n当前 Base URL: {current_base_url}")
    base_url_input = input(f"请输入 Base URL (直接回车使用默认值): ").strip()
    base_url = base_url_input if base_url_input else current_base_url

    # 获取 Model Name
    current_model = existing_config.get("model_name", DEFAULT_MODEL_NAME)
    print(f"\n当前模型名称: {current_model}")
    model_input = input(f"请输入模型名称 (直接回车使用默认值): ").strip()
    model_name = model_input if model_input else current_model

    # 保存配置
    config = {
        "api_key": api_key,
        "base_url": base_url,
        "model_name": model_name
    }

    save_config(config)

    config_path = get_config_path()
    print(f"\n✅ 配置已保存到: {config_path}")
    print("\n配置信息:")
    print(f"  API Key: {api_key[:8]}...{api_key[-4:]}")
    print(f"  Base URL: {base_url}")
    print(f"  模型名称: {model_name}")
    print("\n现在可以使用 'aisk \"你的需求\"' 来生成命令了！")


def main() -> None:
    """初始化命令入口"""
    try:
        init_config()
    except KeyboardInterrupt:
        print("\n\n已取消配置。")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 配置过程中出现错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
