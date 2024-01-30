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
app = FastAPI()
# 初始化模版
templates = Jinja2Templates(directory="templates")
# 登陆验证
security = HTTPBasic()


# 验证中间件
def middleware_http_basic(credentials: HTTPBasicCredentials = Depends(security)):
    current_username = credentials.username
    user = util.osnvironget("BasicUser")
    if user is None:
        user = "zzqqw"
    current_password = credentials.password
    pwd = util.osnvironget("BasicPwd")
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
    palWorldSettings = PalWorldSettings()
    form = palWorldSettings.RenderForm()
    return templates.TemplateResponse("config.html", {"request": request,
                                                      "form": form,
                                                      "palWorldSettingsFile": palWorldSettings.palWorldSettingsFile})


@app.post("/config")
async def index(request: Request, username: str = Depends(middleware_http_basic)):
    form_data = await request.form()
    palWorldSettings = PalWorldSettings()
    palWorldSettings.WriteConfig(dict(form_data))
    form = palWorldSettings.RenderForm()
    return templates.TemplateResponse("config.html", {"request": request,
                                                      "form": form,
                                                      "palWorldSettingsFile": palWorldSettings.palWorldSettingsFile,
                                                      "code": 200})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
