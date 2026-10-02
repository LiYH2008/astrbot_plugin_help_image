# AstrBot 自定义帮助图片插件

`astrbot_plugin_help_image` 会在机器人收到 `help` 指令时，发送插件内置的一张自定义帮助图片。它不需要额外配置，也没有第三方 Python 依赖。

## 功能与工作方式

- 指令处理器由 `@filter.command("help")` 注册；在 AstrBot 使用默认命令前缀时，发送 `/help` 即可触发。
- 插件运行时会以 `main.py` 所在目录为基准，而不是依赖 AstrBot 的安装位置，因此移动或部署到其他环境后仍能正确定位图片。
- 图片查找顺序固定：先读取 `images/custom_help.png`；若文件不存在，再读取 `images/custom_help.jpg`。
- 找到图片后，插件用 AstrBot 的 `Comp.Image.fromFileSystem(...)` 构造图片消息并发送。
- 两个文件都不存在时，插件会记录错误日志，并在聊天中返回实际尝试读取的路径，便于排查。

当前项目自带的是 `images/custom_help.png`，所以现状下 `/help` 会发送这张 PNG 图片。

## 环境要求

- AstrBot `>=4.17.0`
- 已在 AstrBot 中接入以下任一平台适配器：`aiocqhttp`、`misskey` 或 `telegram`

`metadata.yaml` 已声明上述最低版本和平台范围；版本不满足时，AstrBot 会提示插件不兼容并阻止加载。

## 部署

### 方式一：从 AstrBot WebUI 安装

1. 下载本项目的 ZIP 包，或在发布后从插件仓库获取安装包。
2. 在 AstrBot WebUI 打开“插件”页面，选择安装本地插件/上传插件包。
3. 选择 ZIP 包并完成安装。
4. 在插件列表中确认插件已加载；如刚更新过文件，点击插件卡片的“重载插件”。

### 方式二：手动放入插件目录

1. 找到 AstrBot 的插件目录：`AstrBot/data/plugins/`。
2. 将整个 `astrbot_plugin_help_image` 文件夹复制到该目录中。最终结构应如下：

   ```text
   AstrBot/
   └─ data/
      └─ plugins/
         └─ astrbot_plugin_help_image/
            ├─ main.py
            ├─ metadata.yaml
            └─ images/
               └─ custom_help.png
   ```

3. 重启 AstrBot，或在 WebUI 的“插件”页面对该插件执行“重载插件”。
4. 使用已接入的平台向机器人发送 `/help` 测试。

> 如果你在 AstrBot 设置中修改了命令前缀，请使用“当前命令前缀 + `help`”。例如前缀设为 `!` 时，使用 `!help`。

## 替换帮助图片

不需要修改 `main.py`。只需替换 `images` 文件夹内的图片，并保持指定文件名。

### 使用 JPG

1. 准备新的 JPG 图片。
2. 将它命名为 `custom_help.jpg`。
3. 覆盖插件目录中的 `images/custom_help.jpg`。
4. 在 AstrBot WebUI 重载插件，然后发送 `/help` 验证。

### 使用 PNG

1. 准备新的 PNG 图片。
2. 将它命名为 `custom_help.png`，放进插件目录的 `images/` 文件夹。
3. 重载插件并发送 `/help` 验证。

PNG 的优先级高于 JPG：若 `custom_help.png` 与 `custom_help.jpg` 同时存在，插件只会发送 PNG。若想继续使用 JPG，请删除或改名 `custom_help.png`。

建议使用适合聊天窗口阅读的清晰图片，并在替换后确认文件扩展名真实匹配图片格式。请不要改动 `images` 文件夹名称，也不要改动 `custom_help.png`、`custom_help.jpg` 以外的文件名规则。

## 使用

插件加载成功后，在已接入的聊天平台中发送：

```text
/help
```

机器人将直接回复自定义帮助图片。该指令不需要参数。

## 常见问题

### 发送 `/help` 没有图片

先确认插件已在 AstrBot 的插件页加载成功，并使用了 AstrBot 当前配置的命令前缀。随后在插件页执行一次“重载插件”。

### 提示“找不到图片文件”

确认下列路径中至少有一个文件存在：

```text
astrbot_plugin_help_image/images/custom_help.png
astrbot_plugin_help_image/images/custom_help.jpg
```

文件名需完全一致。插件日志会显示实际读取的完整路径，可据此确认文件是否被放到了正确的插件目录。

### 修改图片后仍显示旧图

确认新文件已覆盖到正在运行的 AstrBot 实例的插件目录，然后在 WebUI 重载插件；必要时重启 AstrBot。若同时存在 PNG 和 JPG，请注意 PNG 会优先被发送。

## 元数据

插件元数据在 `metadata.yaml` 中维护，当前声明：

- 支持平台：`aiocqhttp`、`misskey`、`telegram`
- AstrBot 版本：`>=4.17.0`
- 仓库：<https://github.com/LiYH2008/astrbot_plugin_help_image>

这些字段使用 AstrBot 官方插件开发文档定义的 `support_platforms` 与 `astrbot_version` 字段。

## 许可证

本项目采用 [GNU Affero General Public License v3.0 or later](LICENSE)（AGPL-3.0-or-later）许可证，完整条款见 [LICENSE](LICENSE)。
