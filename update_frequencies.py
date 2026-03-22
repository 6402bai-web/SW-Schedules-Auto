import requests
import os
from datetime import datetime, timezone

# ── 数据源配置 ──────────────────────────────────────────────
# EiBi 赛季文件列表（按优先级尝试，自动适配当前赛季）
SEASON_URLS = [
    "http://www.eibispace.de/dx/sked-b25.csv",  # 2025/26 冬季
    "http://www.eibispace.de/dx/sked-a25.csv",  # 2025 夏季
    "http://www.eibispace.de/dx/sked-b24.csv",  # 备用
]

# ── 分类配置（可自由扩展）──────────────────────────────────
TARGETS = {
    "languages": [
        "Chinese", "English", "Japanese", "Korean", "Thai",
        "French", "Spanish", "Arabic", "Russian", "German",
        "Hindi", "Portuguese", "Vietnamese",
    ],
    "countries": [
        "China", "USA", "Japan", "South Korea", "North Korea",
        "UK", "Russia", "Germany", "France", "India",
        "Australia", "Iran", "Cuba",
    ],
}

TABLE_HEADER = (
    "| 频率 (kHz) | 时间 (UTC) | 电台名称 | 语言 | 目标区域 |\n"
    "| :--- | :--- | :--- | :--- | :--- |\n"
)


def fetch_data() -> list[str]:
    """尝试多个赛季 URL，返回成功的数据行列表。"""
    headers = {"User-Agent": "Mozilla/5.0 SW-Schedules-Auto/2.0"}
    for url in SEASON_URLS:
        try:
            print(f"⏳ 尝试获取: {url}")
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            lines = resp.text.splitlines()
            if len(lines) > 10:  # 基本有效性检查
                print(f"✅ 数据获取成功，共 {len(lines)} 行")
                return lines, resp.text
        except Exception as e:
            print(f"⚠️  {url} 失败: {e}")
    raise RuntimeError("❌ 所有数据源均不可用，请检查网络或更新 SEASON_URLS")


def parse_line(line: str) -> dict | None:
    """解析 CSV 行，返回字段字典；格式不符返回 None。"""
    parts = line.split(";")
    if len(parts) < 7:
        return None
    return {
        "khz":     parts[0].strip(),
        "time":    parts[1].strip(),
        "days":    parts[2].strip(),
        "country": parts[3].strip(),
        "station": parts[4].strip(),
        "lang":    parts[5].strip(),
        "area":    parts[6].strip(),
    }


def write_category_file(path: str, title: str, matches: list[str], now_str: str):
    """将匹配行写入 Markdown 文件。"""
    rows = []
    for line in matches:
        p = parse_line(line)
        if p:
            rows.append(
                f"| {p['khz']} | {p['time']} | {p['station']} | {p['lang']} | {p['area']} |"
            )

    if not rows:
        return  # 无有效数据则跳过

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write(f"# 📡 {title} 频率汇总表\n\n")
        f.write(f"> 最后更新时间：{now_str}（UTC）\n\n")
        f.write(f"共收录 **{len(rows)}** 条频率记录。\n\n")
        f.write(TABLE_HEADER)
        f.write("\n".join(rows) + "\n")
    print(f"✅ 已生成: {path}（{len(rows)} 条）")


def main():
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"🚀 开始更新 | {now_str}\n")

    lines, raw_text = fetch_data()

    # 生成分类文件
    total_files = 0
    for category, keywords in TARGETS.items():
        os.makedirs(category, exist_ok=True)
        for word in keywords:
            matches = [l for l in lines if word.lower() in l.lower()]
            if matches:
                path = f"{category}/{word.lower().replace(' ', '_')}.md"
                write_category_file(path, word, matches, now_str)
                total_files += 1

    # 保存原始 CSV
    with open("raw.csv", "w", encoding="utf-8-sig") as f:
        f.write(raw_text)
    print(f"\n📦 原始数据已保存至 raw.csv")

    # 生成汇总索引
    write_index(now_str, total_files, len(lines))
    print(f"\n🎉 全部完成！共生成 {total_files} 个分类文件。")


def write_index(now_str: str, total_files: int, total_lines: int):
    """生成 INDEX.md 汇总索引页。"""
    lines_out = [
        "# 📡 全球短波频率数据库索引\n",
        f"> 最后更新：{now_str}\n",
        f"> 原始数据共 {total_lines} 行 | 分类文件 {total_files} 个\n\n",
        "## 按语言分类\n\n",
    ]
    for word in TARGETS["languages"]:
        path = f"languages/{word.lower().replace(' ', '_')}.md"
        if os.path.exists(path):
            lines_out.append(f"- [{word}]({path})\n")
    lines_out.append("\n## 按国家分类\n\n")
    for word in TARGETS["countries"]:
        path = f"countries/{word.lower().replace(' ', '_')}.md"
        if os.path.exists(path):
            lines_out.append(f"- [{word}]({path})\n")

    with open("INDEX.md", "w", encoding="utf-8") as f:
        f.writelines(lines_out)
    print("📋 已生成索引: INDEX.md")


if __name__ == "__main__":
    main()
