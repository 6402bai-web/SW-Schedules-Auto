import pandas as pd
import requests
import os

# 赛季 URL
SOURCE_URL = "http://www.eibispace.de/dx/sked-b25.csv"

def main():
    # 1. 确保目录存在
    os.makedirs('languages', exist_ok=True)
    os.makedirs('countries', exist_ok=True)
    
    print("正在获取数据...")
    try:
        # 2. 下载原始数据
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=60)
        
        # 3. 核心修正：EiBi 数据其实是用分号 ';' 分隔的
        # 我们直接用文本处理的方式来筛选，这样最稳
        lines = response.text.splitlines()
        
        # 定义我们要抓取的关键词
        targets = {
            'languages': ['Chinese', 'English', 'Japanese'],
            'countries': ['China', 'USA', 'Japan', 'France']
        }

        # 准备一个简单的表头
        header = "kHz;Time(UTC);Days;ITU;Station;Lng;Target;Remarks;P;Start;Stop\n"

        # 开始分类
        for category, keywords in targets.items():
            for word in keywords:
                # 筛选包含关键词的行
                filtered_lines = [line for line in lines if word.lower() in line.lower()]
                
                if filtered_lines:
                    file_path = f"{category}/{word.lower()}.csv"
                    with open(file_path, "w", encoding="utf-8-sig") as f:
                        f.write(header) # 加上表头
                        f.write("\n".join(filtered_lines))
                    print(f"✅ 已整理: {file_path} (共 {len(filtered_lines)} 条记录)")

        # 同时也保存一份原始文件供参考
        with open("raw.csv", "w", encoding="utf-8-sig") as f:
            f.write(response.text)

        print("\n🚀 所有数据整理完毕！请去主页查看文件夹。")
            
    except Exception as e:
        print(f"❌ 运行错误: {e}")

if __name__ == "__main__":
    main()