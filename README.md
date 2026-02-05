# aisk 🚀

**aisk** 是一个基于 AI 的终端命令助手。只需用自然语言描述你的需求，它就能为你生成相应的 Shell 命令，并支持一键执行。

## ✨ 特性

* **自然语言转命令**：不再需要苦记复杂的 `tar`、`find` 或 `ffmpeg` 参数。
* **交互式执行**：生成命令后，你可以选择立即执行、复制或取消。
* **高度可配置**：支持自定义 API Key、Base URL 以及模型（默认支持通义千问）。
* **轻量快捷**：基于 Python 开发，极速响应。

---

## 📦 安装

### 方式 1：直接通过 PyPI 安装 (推荐)

这是最简单的安装方式，适用于大多数用户：

```bash
pip install aisk

```

### 方式 2：从源码安装

如果你想参与开发或尝试最新版本：

```bash
git clone https://github.com/it-zhouyu/aisk.git
cd aisk
pip install .

```

---

## ⚙️ 配置

在使用之前，请确保你已配置环境变量。建议将以下内容添加到你的 `.zshrc` 或 `.bash_profile` 中：

```bash
# 必填：你的 API Key
export ASK_API_KEY="your_api_key_here"

# 选填：自定义 Base URL (默认为通义千问)
export ASK_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"

# 选填：自定义模型 (默认为 qwen-max)
export ASK_MODEL_NAME="qwen-max"

```

---

## 💡 使用方法

直接在终端输入 `aisk` 加上你的需求：

### 1. 查找文件

```bash
aisk 帮我找到当前目录下所有大于 100MB 的 mp4 文件

```

### 2. 压缩/解压

```bash
aisk 把当前文件夹打包成 tar.gz 格式，排除 node_modules

```

### 3. 系统操作

```bash
aisk 查看并杀死占用 8080 端口的进程

```

---

## 🛠 交互逻辑

生成命令后，`aisk` 会提示：

* **Enter** 或 **Y**: 确认并立即执行命令。
* **N**: 取消执行。
* **Esc/其他**: 退出程序。

---

## 📄 开源协议

本项目采用 [MIT](https://www.google.com/search?q=LICENSE) 协议。

---

### 🤝 贡献

如果你有任何改进建议，欢迎提交 Issue 或 Pull Request！

**Made with ❤️ by [it_zhouyu**](mailto:497269678@qq.com)