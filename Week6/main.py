from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware  
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import mysql.connector

# 初始化 FastAPI
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
app.mount("/static", StaticFiles(directory="static"), name = "static")
templates = Jinja2Templates(directory="templates")

# MySQL 連線設定
def get_db_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "8745",
        database = "website"
    )

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signup")
def signup(request: Request, name: str = Form(...), username: str = Form(...), password: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 檢查 username 是否已存在
    cursor.execute("SELECT * FROM member WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        db.close()
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "此帳號已重複",
            "error_type": "signup"  # 標記錯誤類型
        })

    # 插入新會員資料
    cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
    db.commit()
    db.close()

    return RedirectResponse("/", status_code=303)


@app.post("/signin")
def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM member WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    db.close()

    if not user:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "帳號或密碼錯誤",
            "error_type": "login"
        })

    # 設定 session 存放會員資訊
    request.session["SIGNED-IN"] = True
    request.session["USER_ID"] = user["id"]
    request.session["NAME"] = user["name"]

    return RedirectResponse("/member", status_code=303)




@app.get("/member")
def member(request: Request):
    user_id = request.session.get("USER_ID")
    if not user_id:
        return RedirectResponse("/")
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # 取得會員名稱
    cursor.execute("SELECT name FROM member WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    # 取得所有留言
    cursor.execute("""
        SELECT message.id, message.content, message.member_id, member.name 
        FROM message 
        JOIN member ON message.member_id = member.id
        ORDER BY message.id DESC
    """)
    messages = cursor.fetchall()
    db.close()

    return templates.TemplateResponse("member.html", {
        "request": request,
        "name": user["name"],
        "user_id": user_id,  # 讓前端知道登入者 ID
        "messages": messages
    })


@app.post("/createMessage")
def create_message(request: Request, content: str = Form(...)):
    user_id = request.session.get("USER_ID")

    if not user_id:
        return RedirectResponse("/", status_code=303)

    db = get_db_connection()
    cursor = db.cursor()

    # 插入新留言
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (user_id, content))
    db.commit()
    db.close()

    return RedirectResponse("/member", status_code=303)

@app.get("/error")
def error(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get("/signout")
def signout(request: Request):
    request.session.clear()  # 清除所有 Session
    return RedirectResponse("/")

@app.post("/deleteMessage")
def delete_message(request: Request, message_id: int = Form(...)):
    user_id = request.session.get("USER_ID")
    if not user_id:
        return RedirectResponse("/")

    db = get_db_connection()
    cursor = db.cursor()

    # 只允許刪除自己的留言
    cursor.execute("DELETE FROM message WHERE id = %s AND member_id = %s", (message_id, user_id))
    db.commit()
    db.close()

    return RedirectResponse("/member", status_code=303)
