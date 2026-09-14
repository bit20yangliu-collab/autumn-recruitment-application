# 安装与首次初始化

目标是让首次使用直接产出可用资料库，不把环境准备变成多轮问答。所有脚本只使用 Python 标准库；没有第三方 `pip` 依赖。若 Codex 环境没有 Python，直接完成脚本描述的等价文件操作，不要求用户另装运行时。

## 安装技能

优先使用当前 Codex/ChatGPT 提供的技能上传或安装入口导入完整 ZIP。支持本地自定义技能目录的环境也可解压后放入 skills 目录；必须保留整个 `autumn-recruitment-application` 文件夹，不能只复制 `SKILL.md`。OpenAI Skills API 接受单个技能 ZIP 或目录文件上传。

安装后执行非阻塞自检：

1. 确认 `SKILL.md`、`assets/profile-template.json`、`scripts/init_profile.py` 和 `scripts/validate_profile.py` 存在。
2. 有可用 Python 时运行 `scripts/preflight.py`；没有时由 Codex 直接检查相同项目。
3. 自检失败只报告具体缺项和修复办法，不要求用户重新确认任务。

## 用户需要准备

- 最新简历 PDF。
- 证件照；如有独立生活照也一并提供。
- 奖项、证书、成绩单和实习证明（可选，但有助于核验名称、等级和日期）。
- 一个用于保存资料库的本地工作区。提醒用户：数据库可能包含身份证号、电话和家庭信息，不应上传到公共仓库或与技能 ZIP 一起分享。

## 浏览器准备

填写网站需要 Codex/ChatGPT 桌面端的计算机使用能力。优先使用用户已配置并已登录的 Chrome、Edge、Brave、Opera 或 Vivaldi；也可使用 `@Browser` 内置浏览器。浏览器扩展安装涉及浏览器权限，必须由用户在界面完成，skill 不能静默安装。

仅在浏览器尚不可用时，依据 OpenAI 官方说明提示一次：

1. 更新 ChatGPT/Codex 桌面应用。
2. 打开 `Settings > Computer Use`；如果目标浏览器未显示，展开更多浏览器。
3. 选择要使用的浏览器，按提示安装所需插件和 ChatGPT 浏览器扩展。
4. 返回设置，确认浏览器状态显示 `Manage`，并启用其开关。
5. 使用安装扩展的同一个浏览器配置文件；在 Codex 对话中通过 `@Edge`、`@Chrome` 等选择浏览器。
6. 第一次访问招聘域名时，Codex 可能显示平台级网站权限提示。常用招聘网站可选择“允许此网站”以免以后重复；不要为了省事默认开放所有网站。
7. 如果本地文件上传失败，在浏览器扩展管理页打开 ChatGPT 扩展详情，启用“允许访问文件 URL”（官方文档明确给出了 Chrome 步骤；其他 Chromium 浏览器如提供同名设置，按对应界面处理），然后重新开始浏览器任务。

官方说明：https://learn.chatgpt.com/zh-Hans/docs/chrome-extension

## 初始化对话

建议用户这样开始：

> 使用 $autumn-recruitment-application 初始化我的求职资料库。这里是最新简历 PDF 和证件照，请先提取信息，再一次性问我缺少的网申字段。

收到简历后立即执行：

1. 运行 `scripts/init_profile.py <工作区>`，或完成等价的幂等目录初始化。
2. 把用户提供的简历和照片复制到新资料库的 `assets/`，绝不复制进技能目录。
3. 提取简历全文并逐页视觉核对，写入有证据支持的字段及来源。
4. 运行 `scripts/validate_profile.py <profile.json>`，修复结构问题。
5. 先交付可用草稿和缺失清单。只有缺失项会阻止当前任务时，才按主题合并为一条问题；暂不提供的字段保留 `null`。
