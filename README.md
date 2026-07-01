# AIBO

AIBO 是一个本地运行的 AI Agent 系统。`aibo-core` 作为常驻核心进程负责会话、工具调用、权限审批、记忆与上下文压缩，`aibo` CLI 和 `aibo-tui` 通过本机 TCP loopback 与核心进程通信。

## 快速启动

### 1. 准备环境

需要 Python 3.12 和 [uv](https://docs.astral.sh/uv/)。

```powershell
uv --version
```

### 2. 安装依赖

```powershell
cd D:\CodexProject\Aibo
uv sync
```

### 3. 配置 API Key

```powershell
Copy-Item .env.example .env
```

然后编辑 `.env`，填入你的 Anthropic API Key：

```env
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. 启动核心进程

打开一个终端运行：

```powershell
uv run aibo-core
```

默认监听 `127.0.0.1:7437`。

### 5. 验证连接

再打开一个终端运行：

```powershell
uv run aibo ping
```

如果连接正常，会返回 `pong`。

### 6. 启动 TUI

```powershell
uv run aibo-tui
```

进入 TUI 后直接输入消息即可开始对话；输入 `/` 可以触发内置 skill 补全。
