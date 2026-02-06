"""模型管理模块"""
import sys
from .config import (
    load_config,
    save_config,
    get_all_models,
    get_current_model_config,
    set_current_model,
    get_config_path
)


def list_models() -> None:
    """列出所有已配置的模型"""
    models = get_all_models()

    if not models:
        print("❌ 还没有配置任何模型，请先运行 'aisk init' 进行配置")
        return

    config = load_config()
    current_model = config.get("current_model", "")

    print("\n已配置的模型:")
    print("=" * 60)

    for idx, model in enumerate(models, 1):
        name = model.get("name", "未知")
        api_key = model.get("api_key", "")
        base_url = model.get("base_url", "")
        model_name = model.get("model_name", "")
        is_current = " [当前]" if name == current_model else ""

        print(f"\n{idx}. {name}{is_current}")
        print(f"   模型: {model_name}")
        print(f"   Base URL: {base_url}")
        if api_key:
            print(f"   API Key: {api_key[:8]}...{api_key[-4:]}")

    print("\n" + "=" * 60)


def switch_model() -> None:
    """交互式切换模型"""
    models = get_all_models()

    if not models:
        print("❌ 还没有配置任何模型，请先运行 'aisk init' 进行配置")
        return

    if len(models) == 1:
        print(f"❌ 当前只有一个模型 '{models[0].get('name')}'，无法切换")
        print("   请先运行 'aisk init' 添加更多模型")
        return

    config = load_config()
    current_model = config.get("current_model", "")

    print("\n可用模型:")
    print("=" * 40)

    for idx, model in enumerate(models, 1):
        name = model.get("name", "未知")
        is_current = " [当前]" if name == current_model else ""
        print(f"{idx}. {name}{is_current}")

    print("\n" + "=" * 40)

    while True:
        choice = input("\n请输入模型编号或名称 (直接回车取消): ").strip()

        if not choice:
            print("已取消切换")
            return

        # 尝试按编号选择
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(models):
                selected_name = models[choice_num - 1].get("name")
                break
        except ValueError:
            pass

        # 尝试按名称选择
        model_names = [m.get("name") for m in models]
        if choice in model_names:
            selected_name = choice
            break

        print("❌ 无效的选择，请重新输入")

    # 切换模型
    if selected_name == current_model:
        print(f"\n✅ '{selected_name}' 已经是当前模型")
        return

    if set_current_model(selected_name):
        print(f"\n✅ 已切换到模型: {selected_name}")

        # 显示新模型信息
        new_config = get_current_model_config()
        print(f"\n当前模型信息:")
        print(f"  模型名称: {new_config.get('model_name')}")
        print(f"  Base URL: {new_config.get('base_url')}")
        api_key = new_config.get('api_key', '')
        if api_key:
            print(f"  API Key: {api_key[:8]}...{api_key[-4:]}")
    else:
        print(f"\n❌ 切换失败")


def main() -> None:
    """model 命令入口"""
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print("用法:")
        print("  aisk model          列出所有模型并交互式切换")
        print("  aisk model -h       显示帮助信息")
        return

    # 显示模型列表并提供切换选项
    list_models()

    models = get_all_models()
    if len(models) > 1:
        switch_model()


if __name__ == "__main__":
    main()
