# AIBO

AIBO 是一个本地运行的 AI Agent 系统，由常驻的 `aibo-core` 负责会话、工具调用、权限审批、记忆与上下文压缩，`aibo` CLI 和 `aibo-tui` 通过本机 TCP loopback 与核心进程通信。

它的目标是提供一个可审计、可扩展、以本地工作流为中心的 Agent 底座，让交互式 TUI、命令行任务、内置技能、子 agent 和安全工具执行都围绕同一套会话与事件协议运转。
