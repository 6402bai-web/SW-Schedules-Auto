import pandas as pd
import requests
import os

# 赛季 URL
SOURCE_URL = "http://www.eibispace.de/dx/sked-b25.csv"

def main():
    # 强制创建目录
    os.makedirs('languages', exist_ok=True)
    os.makedirs('countries', exist_ok=True)
    
    print(f"正在从 {SOURCE_URL} 获取数据...")
    try:
        # 下载数据
        response = requests.get(SOURCE_URL, timeout=30)
        with open("raw.csv", "wb") as f:
            f.write(response.content)
            
        # 读取数据 (EiBi 格式)
        df = pd.read_csv("raw.csv", encoding='latin-1', header=None, on_bad_lines='skip')
        df.columns = ['kHz', 'Time', 'Days', 'Target', 'Language', 'Station', 'Power', 'Azimuth', 'Location', 'Country']
        
        # 分类逻辑
        langs = ['Chinese', 'English', 'Japanese']
        counts = ['China', 'USA', 'Japan']
        
        for l in langs:
            sub = df[df['Language'].str.contains(l, na=False, case=False)]
            sub.to_csv(f'languages/{l.lower()}.csv', index=False, encoding='utf-8-sig')
            print(f"写入语言文件: {l}")

        for c in counts:
            sub = df[df['Country'].str.contains(c, na=False, case=False)]
            sub.to_csv(f'countries/{c.lower()}.csv', index=False, encoding='utf-8-sig')
            print(f"写入国家文件: {c}")
            
        print("本地文件生成完毕。")
    except Exception as e:
        print(f"运行错误: {e}")

if __name__ == "__main__":
    main()
