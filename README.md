# Elementor MCP Migration Playbook

通过 MCP 将静态页面组织为可编辑的 Elementor 原生区块：执行步骤、编辑边界、动效实现和核对清单。

本仓库只保留通用方法与连接工具，不分发任何特定网站的域名、品牌、页面文案、文章、截图、原始站点源码、页面 ID 或配置备份。

## 文件

- [执行步骤](执行步骤.md)：发现能力、拆分区块、共享样式、文章模型、验收和发布。
- [编辑约束](编辑约束.md)：原生内容与 JS 的职责边界。
- [核对清单](核对清单.md)：排版、交互、可访问性及运营检查。
- `mcp_client.py`：从本机环境变量或 Codex 配置读取 MCP 连接；不含默认目标地址。
- `verify.py`：不访问网络的本地自检。

## 本地自检

Python 3.11+：

```sh
python -m pip install -r requirements.txt
python verify.py
```

## 检查自己的 MCP 连接

在本机 Codex 中配置 Elementor MCP 后，将 MCP_SERVER 设置为该配置的名称，再运行：

```sh
python mcp_client.py
```

也支持 MCP_URL 和 MCP_AUTHORIZATION 环境变量。凭据只存在本机配置或当前会话中；不提交到仓库。该命令只初始化连接并列出工具，不修改网站。

没有通用页面 ID，也没有可直接覆盖任意站点的发布命令。每个目标必须重新发现区块 schema、创建文档并建立自己的映射。
