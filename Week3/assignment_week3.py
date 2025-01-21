import json
import ssl
import urllib.request as req
import re
import csv

# 設定 API URL
urls = [
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1",
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
]

# 建立不驗證 SSL 的 context
context = ssl._create_unverified_context()

# 讀取 JSON 資料的函數
def fetch_json(url):
    with req.urlopen(url, context=context) as f:
        return json.loads(f.read().decode('utf-8'))

# 提取區名的函數
def extract_district(address):
    match = re.search(r'[\u4e00-\u9fa5]+區', address)
    return match.group(0).strip().replace("市", "") if match else "區名未找到"

# 讀取兩個 URL 的資料
json_data1 = fetch_json(urls[0])
json_data2 = fetch_json(urls[1])

# 建立 address_dict 字典
address_dict = {item["SERIAL_NO"]: item["address"] for item in json_data2["data"]}

# 處理景點資料並寫入 'spot.csv'
with open('spot.csv', mode='w', newline='', encoding='utf-8-sig') as file:  # 使用 'utf-8-sig' 編碼
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL, escapechar='\\')  # 使用 'escapechar'
    writer.writerow(['SpotTitle', 'District', 'Longitude', 'Latitude', 'ImageURL'])
    
    for item in json_data1["data"]["results"]:
        stitle = item["stitle"].replace('"', '').strip()
        serial_no = item["SERIAL_NO"]
        address = address_dict.get(serial_no, "地址未找到")
        district = extract_district(address)
        img_data = item.get("filelist", "")
        
        # 提取第一張圖片的 URL
        img_website = next(("https://" + url for url in img_data.split("https://") if url), "")
        
        # 只寫入有內容的列
        row = [stitle, district, item["longitude"], item["latitude"], img_website]
        writer.writerow([value for value in row if value])  # 去掉空值

print("資料已成功寫入 'spot.csv'")

# 建立 address_dict 字典，將 MRT 資料建立字典
address_dict = {item["SERIAL_NO"]: item["MRT"] for item in json_data2["data"]}

# 用於存儲每個捷運站的所有景點
mrt_attractions = {}

# 處理並整理景點資料
for item in json_data1["data"]["results"]:
    serial_no = item["SERIAL_NO"]
    stitle = item["stitle"].replace('"', '').strip()
    
    MRT = address_dict.get(serial_no, "未提供捷運站")
    
    if MRT not in mrt_attractions:
        mrt_attractions[MRT] = []
    
    mrt_attractions[MRT].append(stitle)

# 處理並寫入 'mrt.csv'，每列都是一個景點，去掉標頭
with open('mrt.csv', mode='w', newline='', encoding='utf-8-sig') as file:  # 使用 'utf-8-sig' 編碼，使用EXCEL開啟CSV較能避免亂碼
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL, escapechar='\\')  # 使用 'escapechar'
    
    # 最多景點數量
    max_attractions = max(len(attractions) for attractions in mrt_attractions.values())
    
    # 輸出每個捷運站的所有景點
    for mrt_station, attractions in mrt_attractions.items():
        # 填充景點，若少於最大景點數則填充空白
        row = [mrt_station] + attractions
        writer.writerow([value for value in row if value])  # 去掉空值

print("資料已成功寫入 'mrt.csv'")



import urllib.request as req_lottery
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def getData(url, csv_writer):
    request = req_lottery.Request(url, headers={
        "cookie": "over18-1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    })

    with req_lottery.urlopen(request) as response:
        data = response.read().decode("utf-8")

    # 解析原始碼，取得文章標題、讚/噓數以及內頁連結
    root = BeautifulSoup(data, "html.parser")
    articles = root.find_all("div", class_="r-ent")
    for article in articles:
        title_tag = article.find("div", class_="title").a
        if title_tag:
            title_text = title_tag.string.strip()
            likes = article.find("div", class_="nrec").string
            likes = likes if likes else "0"
            article_url = "https://www.ptt.cc" + title_tag['href']

            # 抓取內頁的發表時間
            with req_lottery.urlopen(req_lottery.Request(article_url, headers={
                "cookie": "over18-1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            })) as inner_response:
                inner_data = inner_response.read().decode("utf-8")
                inner_root = BeautifulSoup(inner_data, "html.parser")
                meta_items = inner_root.find_all("div", class_="article-metaline")
                for item in meta_items:
                    if item.find("span", class_="article-meta-tag").string == "時間":
                        time_str = item.find("span", class_="article-meta-value").string
                        post_time = datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y")
                        formatted_time = post_time.strftime("%a %b %d %H:%M:%S %Y")
                        # 寫入 CSV
                        csv_writer.writerow([title_text, likes, formatted_time])
                        break

    # 往前抓取網頁
    nextLink = root.find("a", string="‹ 上頁")
    return nextLink["href"]

url_lottery = "https://www.ptt.cc/bbs/Lottery/index.html"
count = 0

# 開啟 CSV 檔案並寫入標題行
with open('article.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["ArticleTitle", "Like/DislikeCount", "PublishTime"])
    
    while count < 3:
        url_lottery = "https://www.ptt.cc" + getData(url_lottery, csv_writer)
        count += 1
print("資料已成功寫入 'article.csv'")