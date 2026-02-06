# aisk 🚀

**aisk** 是一个基于 AI 的终端命令助手。只需用自然语言描述你的需求，它就能为你生成相应的 Shell 命令，并支持一键执行。

## ✨ 特性

* **自然语言转命令**：不再需要苦记复杂的 `tar`、`find` 或 `ffmpeg` 参数
* **智能平台识别**：自动识别操作系统（Windows/macOS/Linux），生成对应平台的命令
* **交互式执行**：生成命令后，可以选择立即执行或取消
* **多模型管理**：支持配置多个 AI 模型，随时切换使用
* **高度可配置**：支持任意 OpenAI 兼容的 API，包括通义千问、OpenAI、DeepSeek 等
* **跨平台支持**：支持 Windows、macOS 和 Linux
* **轻量快捷**：基于 Python 开发，极速响应

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

### 初始化配置

在使用之前，需要先进行初始化配置：

```bash
aisk init
```

交互式配置向导会引导你完成以下设置：

- **配置名称**（必填）：为这个模型配置起个名字，方便识别（如 `qwen`、`gpt4` 等）
- **API Key**（必填）：你的 AI 服务 API Key
- **Base URL**（选填）：API 地址，默认为通义千问 `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **模型名称**（选填）：使用的模型，默认为 `qwen3-max`

配置文件会保存到 `~/.aisk/config.json`。

**支持任意 OpenAI 兼容的 API**，包括通义千问、OpenAI、DeepSeek 等。

### 多模型管理

你可以配置多个模型，方便在不同场景下切换：

```bash
# 添加通义千问模型
aisk init
# 输入配置名称: qwen

# 添加 OpenAI 模型
aisk init
# 输入配置名称: gpt4

# 列出所有模型并切换
aisk model
```

运行 `aisk model` 后会显示所有已配置的模型，并支持交互式切换：

```
已配置的模型:
============================================================

1. qwen [当前]
   模型: qwen3-max
   Base URL: https://dashscope.aliyuncs.com/compatible-mode/v1
   API Key: sk-xxxx...xxxx

2. gpt4
   模型: gpt-4
   Base URL: https://api.openai.com/v1
   API Key: sk-yyyy...yyyy

============================================================

请输入模型编号或名称 (直接回车取消):
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

生成命令后，`aisk` 会提示是否执行：

* **Enter** 或 **Y**：确认并立即执行命令
* **N**：取消执行
* **Esc**：退出程序

---

## 📄 开源协议

本项目采用 [MIT](https://www.google.com/search?q=LICENSE) 协议。

---

### 🤝 贡献

如果你有任何改进建议，欢迎提交 Issue 或 Pull Request！

**Made with ❤️ by [it_zhouyu](mailto:497269678@qq.com)**