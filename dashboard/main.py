import logging
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, Response, RedirectResponse
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


# 登录验证中间件
def middlewareHTTPBasic():
    if util.dashboard_env() is False:
        return Depends(HTTPBasic) 
    else:
        def verify(credentials: HTTPBasicCredentials = Depends(security)):
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
        return Depends(verify)



@app.get("/")
async def getConfig(request: Request):
    return RedirectResponse(url="/config")


@app.get("/config", response_class=HTMLResponse)
async def getConfig(request: Request, username: str = middlewareHTTPBasic()):
    palWorldSettings = PalWorldSettings()
    try:
        form = palWorldSettings.RenderForm()
        palWorldSettingsFile = palWorldSettings.palWorldSettingsFile
        code = 100
    except FileNotFoundError as e:
        logging.error("rendering config template: %s", e)
        form = {}
        palWorldSettingsFile = ""
        code = 500
    return templates.TemplateResponse("config.html", {
        "request": request,
        "form": form,
        "palWorldSettingsFile": palWorldSettingsFile,
        "code": code,
        "submitbuttontitle": palWorldSettings.readerSubmitButtonTitle()
    })


@app.post("/config")
async def postConfig(request: Request, username: str = middlewareHTTPBasic()):
    form_data = await request.form()
    palWorldSettings = PalWorldSettings()
    submitButtonTitle = palWorldSettings.readerSubmitButtonTitle()
    try:
        configStr = palWorldSettings.configStr(dict(form_data))
        form = palWorldSettings.RenderForm()
        palWorldSettingsFile = palWorldSettings.palWorldSettingsFile
        code = 200
    except BaseException as e:
        logging.error("submit to config: %s", e)
        form = {}
        palWorldSettingsFile = ""
        code = 201
        configStr = ""
    if submitButtonTitle == "下载配置":
        return Response(
            content=configStr,
            media_type="text/plain",
            headers={
                "Content-Disposition": f"attachment; filename=" + palWorldSettings.palWorldSettingsFileName
            }
        )
    else:
        try:
            palWorldSettings.writeConfig(configStr)
        except BaseException as e:
            logging.error("writeConfig to config: %s", e)
            form = {}
            palWorldSettingsFile = ""
            code = 201
        return templates.TemplateResponse("config.html", {
            "request": request,
            "form": form,
            "palWorldSettingsFile": palWorldSettingsFile,
            "code": code,
            "submitbuttontitle": submitButtonTitle
        })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
