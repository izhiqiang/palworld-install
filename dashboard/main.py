import logging
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from fastapi.templating import Jinja2Templates

import util
from palworld.PalWorldSettings import PalWorldSettings
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()
# 日志级别
logging.basicConfig(level=logging.DEBUG)
# 初始化fastapi
app = FastAPI(docs_url=None, redoc_url=None)
# 初始化模版
templates = Jinja2Templates(directory="templates")
# 登陆验证
security = HTTPBasic()


# 验证中间件
def middleware_http_basic(credentials: HTTPBasicCredentials = Depends(security)):
    current_username = credentials.username
    user = util.osnvironget("DASHBOARD_BASICUSER")
    if user is None:
        user = "dashboard"
    current_password = credentials.password
    pwd = util.osnvironget("DASHBOARD_BASICPWD")
    if pwd is None:
        pwd = "123456"
    if current_password == pwd and current_username == user:
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


@app.get("/config", response_class=HTMLResponse)
async def index(request: Request, username: str = Depends(middleware_http_basic)):
    try:
        palWorldSettings = PalWorldSettings()
        form = palWorldSettings.RenderForm()
        palWorldSettingsFile = palWorldSettings.palWorldSettingsFile
        code = 100
    except:
        form = {}
        palWorldSettingsFile = ""
        code = 500
    return templates.TemplateResponse("config.html", {
        "request": request,
        "form": form,
        "palWorldSettingsFile": palWorldSettingsFile,
        "code": code,
    })


@app.post("/config")
async def index(request: Request, username: str = Depends(middleware_http_basic)):
    form_data = await request.form()
    try:
        palWorldSettings = PalWorldSettings()
        palWorldSettings.WriteConfig(dict(form_data))
        form = palWorldSettings.RenderForm()
        palWorldSettingsFile = palWorldSettings.palWorldSettingsFile
        code = 200
    except:
        form = {}
        palWorldSettingsFile = ""
        code = 201
    return templates.TemplateResponse("config.html", {
        "request": request,
        "form": form,
        "palWorldSettingsFile": palWorldSettingsFile,
        "code": code
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
