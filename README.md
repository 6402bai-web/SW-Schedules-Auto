# 📡 全球短波频率自动汇总 (SW-Schedules-Auto)

![Auto Update](https://github.com/6402bai-web/SW-Schedules-Auto/actions/workflows/auto_update.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

本项目每日自动从 [EiBi Space](http://www.eibispace.de/) 抓取全球短波电台频率数据，
并按**国家**和**语言**分类整理为 Markdown 表格，方便查阅。

> 📅 数据每日自动更新，由 GitHub Actions 驱动。

---

## 📂 目录结构

```
SW-Schedules-Auto/
├── languages/          # 按语言分类（中文、英语、日语等）
├── countries/          # 按国家分类（中国、美国、日本等）
├── INDEX.md            # 所有分类文件的汇总索引
├── raw.csv             # 原始 EiBi CSV 数据备份
├── update_frequencies.py  # 核心更新脚本
└── .github/workflows/  # GitHub Actions 自动化配置
```

---

## 🌍 支持的分类

### 语言
中文 · 英语 · 日语 · 韩语 · 泰语 · 法语 · 西班牙语 · 阿拉伯语 · 俄语 · 德语 · 印地语 · 葡萄牙语 · 越南语

### 国家/地区
中国 · 美国 · 日本 · 韩国 · 朝鲜 · 英国 · 俄罗斯 · 德国 · 法国 · 印度 · 澳大利亚 · 伊朗 · 古巴

---

## 📊 数据格式

每个分类文件包含以下字段：

| 字段 | 说明 |
| :--- | :--- |
| 频率 (kHz) | 短波频率，单位千赫兹 |
| 时间 (UTC) | 播出时间段（UTC） |
| 电台名称 | 广播电台名称 |
| 语言 | 播出语言 |
| 目标区域 | 目标收听地区 |

---

## 🚀 本地运行

```bash
# 克隆项目
git clone https://github.com/6402bai-web/SW-Schedules-Auto.git
cd SW-Schedules-Auto

# 安装依赖
pip install -r requirements.txt

# 运行更新脚本
python update_frequencies.py
```

---

## ⚙️ 自动化说明

本项目使用 **GitHub Actions** 每日 UTC 00:00 自动运行更新脚本，
并将生成的文件自动提交回仓库。

脚本会按优先级尝试多个赛季数据源，自动适配当前 EiBi 赛季，无需手动修改 URL。

---

## 📜 数据来源

- **EiBi Space**：[http://www.eibispace.de/](http://www.eibispace.de/)
- 数据版权归 EiBi Space 所有，本项目仅作整理展示用途。

---

## 🤝 贡献

欢迎提交 Issue 或 PR！
- 想添加新的语言/国家分类？修改 `update_frequencies.py` 中的 `TARGETS` 字典即可。
- 发现数据问题？请提 Issue。

---

*Powered by [GitHub Actions](https://github.com/features/actions) · Data from [EiBi Space](http://www.eibispace.de/)*
