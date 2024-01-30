import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from palworld.PalWorldSettings import PalWorldSettings
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()
# 日志级别
logging.basicConfig(level=logging.DEBUG)
# 初始化fastapi
app = FastAPI()
# 初始化模版
templates = Jinja2Templates(directory="templates")


@app.get("/config", response_class=HTMLResponse)
async def index(request: Request):
    palWorldSettings = PalWorldSettings()
    form = palWorldSettings.RenderForm()
    return templates.TemplateResponse("config.html", {"request": request, "form": form})


@app.post("/config")
async def index(request: Request):
    form_data = await request.form()
    palWorldSettings = PalWorldSettings()
    palWorldSettings.WriteConfig(dict(form_data))
    form = palWorldSettings.RenderForm()
    return templates.TemplateResponse("config.html", {"request": request, "form": form, "code": 200})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
