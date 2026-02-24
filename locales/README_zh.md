# 翻译说明

**[English](README.md)**

## 更新 .pot 模板

在项目**根目录**下执行，可重新生成基础 .pot 文件：

```bash
pygettext3.9 -d guess -o locales/openmatb.pot *
```

也可使用 [Poedit](https://poedit.net/) 等 PO 编辑器的“从源码检测”功能。

## 编辑与存放

- 使用 Poedit 等软件编辑 .po 文件。
- 新语言的翻译文件（.po 与 .mo）请放在：
  - `locales/xx_XX/LC_MESSAGES/`
  - 文件名分别为：`openmatb.po`、`openmatb.mo`
- `xx_XX` 为语言/地区代码（见下方或 [locale 代码列表](https://stackoverflow.com/questions/3191664/list-of-all-locales-and-their-short-codes)）。

## 编译 .mo

安装 Babel 后，在项目根目录执行（将 `zh_Hans_CN` 换成你的语言代码）：

```bash
pybabel compile -D openmatb -d locales -l zh_Hans_CN
```

## 本项目常用语言代码

| 代码 | 语言 |
|------|------|
| en_EN | 英语 |
| fr_FR | 法语 |
| zh_Hans_CN | 简体中文（中国） |
| zh_Hant_TW | 繁体中文（台湾） |
| ja_JP | 日语 |
| ko_KR | 韩语 |

完整 locale 代码列表见同目录下的英文 [README.md](README.md)。
