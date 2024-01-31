## 在线管理配置配置中心

~~~
pip3 install -r requirements.txt 
python3 main.py 
启动服务端口: 8000
~~~

> 配置中心修改路由
>
> http://127.0.0.1:8000/config

## 环境变量

~~~
//游戏安装目录
PALSERVERPATH=/home/steam/Steam/steamapps/common/PalServer/
//前端表单显示的input以及提交进行校验参数
FORMJSON_PALWORLDSETTINGS=./form/PalWorldSettings.json
//修改完成之后，重启服务命令
RESTARTPALSERVER_COMMAND="sudo systemctl restart pal-server"
//登陆账号
DASHBOARD_BASICUSER="dashboard"
// 登陆密码
DASHBOARD_BASICPWD="123456"
~~~

> PalWorldSettings.ini
>
> /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini