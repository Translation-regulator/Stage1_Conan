from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware  
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signin")
def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    if not username or not password:
        return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=302)
    if username == "test" and password == "test":
        request.session["SIGNED-IN"] = True
        return RedirectResponse("/member", status_code=302)
    return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=302)


@app.get("/member")
def member(request: Request):
    if request.session.get("SIGNED-IN"):
        return templates.TemplateResponse("member.html", {"request": request})
    return RedirectResponse("/")

@app.get("/error")
def error(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get("/signout")
def signout(request: Request):
    request.session.clear()
    return RedirectResponse("/")

@app.get("/square/{number}")
def square(number: int, request: Request):
    squared = number ** 2
    return templates.TemplateResponse("square.html", {"request": request, "number": number, "squared": squared})

