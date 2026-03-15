import pandas as pd
import requests
import os

# 1. 自动获取当前赛季的 URL (2026年3月目前是 B25 季)
SOURCE_URL = "http://www.eibispace.de/dx/sked-b25.csv"

# 2. 定义你想分类的列表（你可以随时在这里添加更多）
LANGUAGES = ['Chinese', 'English', 'Japanese', 'Korean', 'French', 'German']
COUNTRIES = ['China', 'USA', 'Japan', 'France', 'Germany', 'Russia']

def setup_env():
    """创建存放数据的文件夹"""
    for folder in ['languages', 'countries']:
        if not os.path.exists(folder):
            os.makedirs(folder)

def main():
    setup_env()
    print(f"正在下载数据源: {SOURCE_URL}")
    
    try:
        # 3. 下载并清洗数据
        # EiBi 的 CSV 没有表头，且编码是 latin-1
        df = pd.read_csv(SOURCE_URL, encoding='latin-1', header=None, on_bad_lines='skip')
        
        # 定义列名 (根据 EiBi 官方格式)
        # 0:kHz, 1:Time(UTC), 4:Language, 5:Station, 9:Country
        df.columns = ['kHz', 'Time', 'Days', 'Target', 'Language', 'Station', 'Power', 'Azimuth', 'Location', 'Country']
        
        # 4. 按语言分类并保存
        print("正在按语言分类...")
        for lang in LANGUAGES:
            filtered = df[df['Language'].str.contains(lang, na=False, case=False)]
            if not filtered.empty:
                filtered.to_csv(f'languages/{lang.lower()}.csv', index=False, encoding='utf-8-sig')

        # 5. 按国家分类并保存
        print("正在按国家分类...")
        for country in COUNTRIES:
            filtered = df[df['Country'].str.contains(country, na=False, case=False)]
            if not filtered.empty:
                filtered.to_csv(f'countries/{country.lower()}.csv', index=False, encoding='utf-8-sig')

        print("🎉 所有分类数据已更新完毕！")

    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    main()
