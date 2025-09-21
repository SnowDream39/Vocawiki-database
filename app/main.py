from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.config import settings
from app.routers.user import router as user_router
from app.routers.entry import router as entry_router


app = FastAPI()

# 全局中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# 挂载子路由
app.include_router(user_router)
app.include_router(entry_router)
