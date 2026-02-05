"""初始化配置模块"""
import sys
from .config import save_config, load_config, get_config_path, get_all_models


DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEFAULT_MODEL_NAME = "qwen-max"


def init_config() -> None:
    """交互式初始化配置"""
    print("🔧 aisk 配置初始化")
    print("=" * 40)

    # 加载现有配置
    config = load_config()
    models = get_all_models()

    # 如果已有模型，询问是添加新模型还是修改现有模型
    if models:
        print(f"\n当前已配置 {len(models)} 个模型")
        add_new = input("\n是否添加新模型? (y/N): ").strip().lower()

        if add_new not in ['y', 'yes']:
            # 修改现有模型
            modify_existing_model(models)
            return

    # 获取模型名称（用于标识）
    print("\n提示: 模型名称用于标识不同的模型配置，例如: qwen, openai, deepseek")
    while True:
        model_alias = input("请输入模型名称 (用于标识): ").strip()
        if model_alias:
            # 检查是否已存在
            existing_names = [m.get("name") for m in models]
            if model_alias in existing_names:
                print(f"❌ 模型名称 '{model_alias}' 已存在，请使用其他名称")
                continue
            break
        print("❌ 模型名称不能为空，请重新输入")

    # 获取 API Key
    while True:
        api_key = input("\n请输入 API Key (必填): ").strip()
        if api_key:
            break
        print("❌ API Key 不能为空，请重新输入")

    # 获取 Base URL
    base_url_input = input(f"\n请输入 Base URL (直接回车使用默认值 {DEFAULT_BASE_URL}): ").strip()
    base_url = base_url_input if base_url_input else DEFAULT_BASE_URL

    # 获取 Model Name
    model_input = input(f"\n请输入模型名称 (直接回车使用默认值 {DEFAULT_MODEL_NAME}): ").strip()
    model_name = model_input if model_input else DEFAULT_MODEL_NAME

    # 创建新模型配置
    new_model = {
        "name": model_alias,
        "api_key": api_key,
        "base_url": base_url,
        "model_name": model_name
    }

    # 更新配置
    models.append(new_model)

    # 如果这是第一个模型，或者没有当前模型设置，设置为当前模型
    if not config.get("current_model"):
        config["current_model"] = model_alias

    config["models"] = models
    save_config(config)

    config_path = get_config_path()
    print(f"\n✅ 模型配置已保存到: {config_path}")
    print("\n新模型信息:")
    print(f"  模型标识: {model_alias}")
    print(f"  API Key: {api_key[:8]}...{api_key[-4:]}")
    print(f"  Base URL: {base_url}")
    print(f"  模型名称: {model_name}")

    is_current = " [当前模型]" if config.get("current_model") == model_alias else ""
    print(f"{is_current}")

    print("\n提示: 使用 'aisk model' 命令可以查看和切换模型")
    print("      使用 'aisk \"你的需求\"' 来生成命令")


def modify_existing_model(models: list) -> None:
    """修改现有模型配置"""
    config = load_config()
    current_model = config.get("current_model", "")

    print("\n现有模型列表:")
    for idx, model in enumerate(models, 1):
        name = model.get("name", "未知")
        is_current = " [当前]" if name == current_model else ""
        print(f"{idx}. {name}{is_current}")

    while True:
        choice = input("\n请选择要修改的模型编号: ").strip()

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(models):
                selected_model = models[choice_num - 1]
                break
        except ValueError:
            pass

        print("❌ 无效的编号，请重新输入")

    model_alias = selected_model.get("name")
    print(f"\n正在修改模型: {model_alias}")
    print("(直接回车保留当前值)")

    # 修改 API Key
    current_api_key = selected_model.get("api_key", "")
    print(f"\n当前 API Key: {current_api_key[:8]}...{current_api_key[-4:]}")
    api_key_input = input("请输入新的 API Key: ").strip()
    if api_key_input:
        selected_model["api_key"] = api_key_input

    # 修改 Base URL
    current_base_url = selected_model.get("base_url", "")
    print(f"\n当前 Base URL: {current_base_url}")
    base_url_input = input("请输入新的 Base URL: ").strip()
    if base_url_input:
        selected_model["base_url"] = base_url_input

    # 修改 Model Name
    current_model_name = selected_model.get("model_name", "")
    print(f"\n当前模型名称: {current_model_name}")
    model_input = input("请输入新的模型名称: ").strip()
    if model_input:
        selected_model["model_name"] = model_input

    # 保存配置
    config["models"] = models
    save_config(config)

    print(f"\n✅ 模型 '{model_alias}' 已更新")


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
