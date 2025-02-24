# FastAPI 初步開發會員系統

## **1. FastAPI 應用初始化**
```python
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware  
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from urllib.parse import urlencode
import mysql.connector
```

### **這段程式碼的功能：**  
- **FastAPI**: 建立 API 服務 (物件)。  
- **Form**: 讓 FastAPI 處理 HTML 表單傳來的資料。  
- **Request**: 存取請求資訊，例如 session。    
- **RedirectResponse**: 讓 API 重新導向特定頁面。  
- **SessionMiddleware**: 讓 FastAPI 支援 session（類似 cookie）。  
- **Jinja2Templates**: 設定 Jinja2 模板，用於渲染 HTML 頁面。  
- **StaticFiles**: 讓 FastAPI 服務靜態檔案（CSS、JS、圖片等）。  
- **urlencode**: 用於處理 URL 編碼，例如錯誤訊息傳遞。  
- **mysql.connector**: 連接 MySQL 資料庫。  

---

## **2. 初始化 FastAPI 應用**
```python
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
```

### **這段程式碼的功能：**  
- **創建 FastAPI 應用 (`app = FastAPI()`)**。  
- **加入 SessionMiddleware**，以便使用 `request.session` 來存儲登入狀態。  
- **掛載靜態檔案目錄 `/static`**，讓網站能夠存取 CSS、JS 等靜態資源。  
- **設定模板目錄 `/templates`**，用於渲染 HTML 頁面。  

---

## **3. MySQL 連線函式**
```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="8745",
        database="website"
    )
```

### **這段程式碼的功能：**  
- **建立 MySQL 連線**，每次需要存取資料庫時都會呼叫這個函式。  

---

## **4. 首頁路由**
```python
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

### **這段程式碼的功能：**  
- **處理 GET 請求 `/`（首頁）**。  
- **回傳 `index.html`，顯示首頁內容**。  

---

## **5. 註冊（/signup）**
```python
@app.post("/signup")
def signup(request: Request, name: str = Form(...), username: str = Form(...), password: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 檢查帳號是否重複
    cursor.execute("SELECT * FROM member WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        db.close()
        error_message = urlencode({"message": "此帳號已重複"})
        return RedirectResponse(f"/error?{error_message}", status_code=303)

    # 插入新會員
    cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
    db.commit()
    db.close()

    return RedirectResponse("/", status_code=303)
```

### **這段程式碼的功能：**  
1. 取得使用者輸入的 `name`、`username`、`password`。  
2. 連線 MySQL，檢查 `username` 是否已存在。  
3. 若帳號已存在，則導向 `/error` 頁面並顯示錯誤訊息。  
4. 若帳號未重複，則新增使用者資料到 `member` 資料表。  
5. 註冊完成後，導向 `/`（首頁）。  

---

## **6. 登入（/signin）**
```python
@app.post("/signin")
def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 查詢是否有匹配的 username & password
    cursor.execute("SELECT * FROM member WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    db.close()

    if not user:
        error_message = urlencode({"message": "帳號或密碼錯誤"})
        return RedirectResponse(f"/error?{error_message}", status_code=303)

    # 記錄登入狀態
    request.session["SIGNED-IN"] = True
    request.session["USER_ID"] = user["id"]
    request.session["NAME"] = user["name"]

    return RedirectResponse("/member", status_code=303)
```

### **這段程式碼的功能：**  
1. 取得 `username` 和 `password`，連線 MySQL 查詢帳號密碼是否匹配。  
2. 若匹配失敗，則導向 `/error` 顯示錯誤訊息。  
3. 若匹配成功，則將登入資訊存入 `session`，並導向 `/member`（會員頁面）。  

---


