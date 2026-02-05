import os
import sys
import tty
import termios
from openai import OpenAI

# 配置环境变量读取
API_KEY = os.getenv("ASK_API_KEY")
BASE_URL = os.getenv("ASK_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
MODEL_NAME = os.getenv("ASK_MODEL_NAME", "qwen-max")

def get_char():
    """读取单个字符，支持 Esc、回车和普通字母"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def get_command(nl_input):
    if not API_KEY:
        return "Error: 请配置环境变量 ASK_API_KEY"
    
    try:
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a macOS terminal expert. Return ONLY the shell command. No markdown, no explanation."},
                {"role": "user", "content": nl_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("用法: aisk '你的需求'")
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