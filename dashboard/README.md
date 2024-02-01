## 在线管理配置配置中心

~~~
apt install python3 python3-pip
pip3 install -r requirements.txt 
python3 main.py 
启动服务端口: 8000
~~~

> 配置中心修改路由
>
> http://127.0.0.1:8000/config

## 守护进程

~~~
apt install -y supervisor

cat > /etc/supervisor/conf.d/palworld.py << EOF
[program:palworld-dashboard]
command = python3 /home/steam/dashboard/main.py
directory=/home/steam/dashboard
stdout_logfile=/home/steam/dashboard/runtime/log.log
stderr_logfile=/home/steam/dashboard/runtime/log-err.log
autorestart=false
startretries=3
user=steam
EOF

// 重启supervisor服务器
service supervisor restart


// 查看进程运行状态
supervisorctl status 
// 启动进程
supervisorctl start palworld-dashboard
// 关闭进程
supervisorctl stop palworld-dashboard
// 重启进程
supervisorctl restart palworld-dashboard
// 重新载入配置文件
supervisorctl update
// 关闭supervisord
supervisorctl shutdown
// 清空进程日志
supervisorctl clear palworld-dashboard
//进入到交互模式下。使用help查看所有命令。
supervisorctl 
~~~

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