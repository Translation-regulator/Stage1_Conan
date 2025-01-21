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

