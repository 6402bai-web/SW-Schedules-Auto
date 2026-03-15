import requests
import os

# 赛季 URL
SOURCE_URL = "http://www.eibispace.de/dx/sked-b25.csv"

def main():
    os.makedirs('languages', exist_ok=True)
    os.makedirs('countries', exist_ok=True)
    
    print("正在获取数据并进行精美排版...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=60)
        lines = response.text.splitlines()
        
        # 定义分类逻辑
        targets = {
            'languages': ['Chinese', 'English', 'Japanese'],
            'countries': ['China', 'USA', 'Japan']
        }

        # Markdown 表格的表头
        table_header = "| 频率 (kHz) | 时间 (UTC) | 电台名称 | 语言 | 目标区域 |\n| :--- | :--- | :--- | :--- | :--- |\n"

        for category, keywords in targets.items():
            for word in keywords:
                # 筛选行
                matches = [line for line in lines if word.lower() in line.lower()]
                
                if matches:
                    file_path = f"{category}/{word.lower()}.md"
                    with open(file_path, "w", encoding="utf-8-sig") as f:
                        f.write(f"# 📡 {word} 频率汇总表\n\n")
                        f.write(f"> 最后更新时间：{os.popen('date').read()}\n\n")
                        f.write(table_header)
                        
                        for line in matches:
                            parts = line.split(';')
                            if len(parts) >= 7:
                                # 提取我们需要的部分（频率、时间、电台、语言、目标区）
                                khz = parts[0]
                                time = parts[1]
                                station = parts[4]
                                lang = parts[5]
                                area = parts[6]
                                f.write(f"| {khz} | {time} | {station} | {lang} | {area} |\n")
                    print(f"✅ 已生成精美表格: {file_path}")

        # 保存原始文件备查
        with open("raw.csv", "w", encoding="utf-8-sig") as f:
            f.write(response.text)
            
    except Exception as e:
        print(f"❌ 运行错误: {e}")

if __name__ == "__main__":
    main()