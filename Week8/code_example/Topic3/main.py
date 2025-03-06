from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ❌ 錯誤設定：只允許 https://example.com
app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],  # 只允許 example.com，其他請求都會被 CORS 拒絕 // 改成 null 允許'file://'發出的請求
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_credentials=True
)

class Item(BaseModel):
    name: str

@app.get("/data")
async def get_data():
    return {"message": "這是來自後端的資料"}

@app.post("/data")
async def post_data(item: Item):
    return {"message": f"已收到 {item.name}"}
