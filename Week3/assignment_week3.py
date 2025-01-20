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
        
        writer.writerow([stitle, district, item["longitude"], item["latitude"], img_website])

print("資料已成功寫入 'spot.csv'.")

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

# 處理並寫入 'mrt.csv'
with open('mrt.csv', mode='w', newline='', encoding='utf-8-sig') as file:  # 使用 'utf-8-sig' 編碼，使用EXCEL開啟CSV較能避免亂碼
    writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL, escapechar='\\')  # 使用 'escapechar'
    writer.writerow(['StationName', 'AttractionTitles'])
    
    for mrt_station, attractions in mrt_attractions.items():
        attractions_str = " ,".join(attractions).replace('"', '').strip()
        writer.writerow([mrt_station, attractions_str])

print("資料已成功寫入 'mrt.csv'.")
