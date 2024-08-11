### docker-compose 

~~~
version: "3.9"

services:
  dedicated-server:
    image: zhiqiangwang/palworld-server:base
    restart: unless-stopped
    network_mode: bridge
    ports:
      - 8211:8211/udp
      - 25575:25575/tcp
    environment:
      - PORT=8211
      - SERVER_NAME=Default Palworld Server
      - SERVER_DESC=Default Palworld Server
      - ADMIN_PASSWORD=steam
      - SERVER_PASSWORD=
      - RCON_ENABLED=true
      - RCON_PORT=25575
      - FORCE_UPDATE=false
      - CLI_ARGS="-useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS"
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./data:/home/steam/Steam/steamapps/common/PalServer/Pal/Saved
      - ./mods:/home/steam/Steam/steamapps/common/PalServer/Pal/Content/Paks/MOD
~~~

### FRP内网穿透

#### frps配置参考

~~~
bindPort = 7001 #{必选} 客户端与该端口建立连接
transport.tls.enable = true

#身份验证
auth.method = "token"  #{可选}身份验证方式
auth.token = "123456" #token设置密码，用于通过身份验证创建连接

#frp服务仪表板配置
webServer.port = 17300  #{也可自行修改端口}
webServer.addr = "0.0.0.0" #公网ip或者域名
webServer.user = "izhiqiang" #登录用户名{可自行修改}
webServer.password = "123456" #登录密码{可自行修改}
~~~

#### frpc配置参考

~~~
serverAddr = "192.168.3.2" #填写你的frps服务器
serverPort = 7001 #填写你的frps服务的端口
auth.token = "123456"
transport.tls.enable = true

[palworld-ucp]
name = "palworld-ucp"
type = "udp"
localIP = "127.0.0.1"
localPort = 8211
remotePort = 8211

[palworld-rcon]
name = "palworld-rcon"
type = "tcp"
localIP = "127.0.0.1"
localPort = 25575
remotePort = 25575
~~~

### RCON服务器指令

steam是PalWorldSettings.ini中`AdminPassword`参数,也就是docker镜像环境变量是`ADMIN_PASSWORD`

~~~
./rcon -a 192.168.3.2:25575 -p steam
~~~

> https://github.com/gorcon/rcon-cli
>
> https://tech.palworldgame.com/server-commands 