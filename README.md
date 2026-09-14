# 秋招简历投递 Skill

`autumn-recruitment-application` 是一个面向 Codex / ChatGPT 的求职网申技能。它会把简历 PDF 和补充资料整理为可维护的本地求职数据库，并在用户给出招聘网址后直接填写校园招聘或实习申请表。

## 主要功能

- 从简历 PDF 初始化结构化求职资料库，并保留信息来源。
- 维护教育、实习、项目、奖项、证书、技能和家庭信息等常见网申字段。
- 用户给出招聘网址后立即开始填写，无需开始前授权或逐字段确认。
- 自动填写资料库中已有的普通与敏感字段、上传简历和照片、保存草稿并进入后续页面。
- 缺失或冲突信息只有在阻塞当前表单时才合并询问一次。
- 出国/境外身份，以及本人或亲属与目标企业及关联机构的关系类问题，默认填写“否”；已有相反事实时以实际信息为准。
- 用户明确说“直接提交”或“直接投递”时，复核后不重复询问；只说“填写”时则停在最终提交前。
- 提供无第三方依赖的初始化、校验和脱敏打包脚本。

## 目录结构

```text
autumn-recruitment-application/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── profile-template.json
├── references/
│   ├── onboarding.md
│   ├── database-guide.md
│   └── form-filling.md
└── scripts/
    ├── preflight.py
    ├── init_profile.py
    ├── validate_profile.py
    └── package_shareable.py
```

## 安装

1. 点击仓库页面的 **Code → Download ZIP**，然后解压。
2. 将目录重命名为 `autumn-recruitment-application`。
3. 把完整目录放入本机 Codex skills 目录，或通过支持技能上传的 Codex / ChatGPT 环境导入。不要只复制 `SKILL.md`。
4. 如需填写已登录的网站，在桌面应用的 **Settings → Computer Use** 中配置 Edge、Chrome 等支持的浏览器，并在对话中使用 `@Edge`、`@Chrome` 等选择它。

本技能的脚本只使用 Python 标准库；没有第三方 `pip` 依赖。没有 Python 时，Codex 也可以直接完成等价的文件初始化和校验。

## 首次初始化

准备最新简历 PDF 和证件照，然后输入：

```text
使用 $autumn-recruitment-application 初始化我的求职资料库。这里是最新简历 PDF 和证件照，请先提取信息并生成可用草稿。
```

默认在当前工作区创建：

```text
job-application-profile/
├── profile.json
├── assets/
└── sources/
```

也可以手动运行：

```bash
python scripts/preflight.py
python scripts/init_profile.py <工作区路径>
python scripts/validate_profile.py <profile.json 路径>
```

## 填写招聘网站

只填写并保存草稿：

```text
使用 $autumn-recruitment-application 根据本地资料库填写这个招聘网址：https://example.com/job
```

复核后直接投递：

```text
使用 $autumn-recruitment-application 填写并直接提交这个职位：https://example.com/job
```

登录密码、验证码和二次验证仍由用户完成。Codex 或浏览器自身显示的站点权限提示属于平台控制，技能不会尝试绕过。

## 隐私与分发

- 真实的 `profile.json`、简历和照片只保存在用户工作区，不应放进技能目录或提交到公共仓库。
- 未知信息保持 `null`，技能不会猜测身份证号、联系方式、日期、亲属关系、薪资或资格声明。
- `package_shareable.py` 只打包明确列入白名单的技能文件；出现额外个人资料或陌生文件时会拒绝打包。
- 对外分享前仍建议检查 ZIP 或仓库内容，确保没有加入个人求职资料。

## 适用范围

本技能用于用户指定的校园招聘和实习网申，不用于自主搜索职位，也不会在用户未要求时主动投递。
