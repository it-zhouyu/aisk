import os
import sys
from openai import OpenAI
from .config import get_api_key, get_base_url, get_model_name, get_config_path


# Windows 和 Unix 系统的字符输入兼容处理
if sys.platform == "win32":
    import msvcrt

    def get_char():
        """读取单个字符 (Windows)"""
        return msvcrt.getch().decode('utf-8')
else:
    import tty
    import termios

    def get_char():
        """读取单个字符，支持 Esc、回车和普通字母 (Unix)"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get_os_description():
    """获取当前操作系统的描述"""
    if sys.platform == "win32":
        return "Windows"
    elif sys.platform == "darwin":
        return "macOS"
    elif sys.platform.startswith("linux"):
        return "Linux"
    else:
        return "Unix-like"

def get_command(nl_input):
    api_key = get_api_key()
    if not api_key:
        return "Error: 请先运行 'aisk init' 进行配置"

    base_url = get_base_url()
    model_name = get_model_name()

    # 获取当前操作系统并动态生成system prompt
    os_type = get_os_description()
    system_prompt = f"You are a {os_type} terminal expert. Return ONLY the shell command for {os_type}. No markdown, no explanation."

    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": nl_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  aisk init            初始化配置")
        print("  aisk model           查看和切换模型")
        print("  aisk '你的需求'       生成命令")
        return

    # 处理 init 子命令
    if sys.argv[1] == "init":
        from .init import main as init_main
        init_main()
        return

    # 处理 model 子命令
    if sys.argv[1] == "model":
        from .model import main as model_main
        model_main()
        return

    user_query = " ".join(sys.argv[1:])
    print(f"🔍 正在检索命令: {user_query}...")

    command = get_command(user_query)

    if command.startswith("Error"):
        print(f"❌ {command}")
        return

    print(f"\n💡 推荐命令: \033[1;32m{command}\033[0m")
    
    # 提示用户，Y 大写表示默认
    print("\n是否立即执行该命令? (Y/n): ", end="", flush=True)

    char = get_char()
    
    # \r 是回车，\n 是换行。如果用户直接按回车，或者输入 y/Y，则执行
    if char in ('\r', '\n', 'y', 'Y'):
        print("Yes") # 回显用户的选择
        print("🚀 正在执行...\n")
        os.system(command)
    # 如果是 Esc (ASCII 27) 或 n/N，则取消
    elif char in (chr(27), 'n', 'N'):
        print("No")
        print("\n已取消执行。")
    else:
        print("\n无效输入，已跳过。")

if __name__ == "__main__":
    main()