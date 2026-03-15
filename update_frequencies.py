import pandas as pd
import requests
import os

# 赛季 URL
SOURCE_URL = "http://www.eibispace.de/dx/sked-b25.csv"

def main():
    # 1. 强制创建目录
    os.makedirs('languages', exist_ok=True)
    os.makedirs('countries', exist_ok=True)
    
    print(f"正在尝试下载: {SOURCE_URL}")
    try:
        # 2. 增加请求头，防止被服务器拒绝
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(SOURCE_URL, headers=headers, timeout=60)
        
        if response.status_code != 200:
            print(f"下载失败，状态码: {response.status_code}")
            return

        # 保存原始文件
        with open("raw.csv", "wb") as f:
            f.write(response.content)
            
        # 3. 读取并处理数据
        df = pd.read_csv("raw.csv", encoding='latin-1', header=None, on_bad_lines='skip')
        # 给列命名
        df.columns = ['kHz', 'Time', 'Days', 'Target', 'Language', 'Station', 'Power', 'Azimuth', 'Location', 'Country']
        
        # 4. 执行分类提取
        langs = {'Chinese': 'chinese.csv', 'English': 'english.csv', 'Japanese': 'japanese.csv'}
        for lang_name, file_name in langs.items():
            sub = df[df['Language'].str.contains(lang_name, na=False, case=False)]
            if not sub.empty:
                sub.to_csv(f'languages/{file_name}', index=False, encoding='utf-8-sig')
                print(f"✅ 已生成语言文件: {file_name}")

        counts = {'China': 'china.csv', 'USA': 'usa.csv', 'Japan': 'japan.csv'}
        for count_name, file_name in counts.items():
            sub = df[df['Country'].str.contains(count_name, na=False, case=False)]
            if not sub.empty:
                sub.to_csv(f'countries/{file_name}', index=False, encoding='utf-8-sig')
                print(f"✅ 已生成国家文件: {file_name}")
            
    except Exception as e:
        print(f"❌ 运行中出现错误: {e}")

if __name__ == "__main__":
    main()
