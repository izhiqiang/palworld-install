## Internationalization Doc

- [Chinese documents](./README.md)
- [English document](./README.EN.md)

## 服务器配置推荐

| 人数   | 推荐配置 |
| ------ | -------- |
| 4～8   | 4核16G   |
| 10～20 | 8核32G   |
| 16～24 | 16核32G  |
| 32     | 16核64G  |

推荐腾讯云游戏专属服务器一个月近需32RMB，[点击我进入购买](https://curl.qcloud.com/Y9Umsuw8)

## 获取方式

### Dokcer环境

~~~
git clone https://github.com/zzqqw/palworld-install.git
cd palworld-install
//单独启动
docker-compose -f docker-compose.base.yml up -d
~~~

### **一键脚本部署环境**
> - 服务器套餐配置：以CPU 4核、内存 16GB为例（通常可以满足6-8人同时在线联机）
> - 操作系统：Ubuntu 22.04 LTS

```shell
wget -O - https://raw.githubusercontent.com/zzqqw/palworld-install/main/sh/install.sh|sh
```
如果您后续想管理该服务，可以参考以下命令来进行：

~~~
# 启动幻兽帕鲁的服务
sudo systemctl start pal-server
# 重启幻兽帕鲁的服务
sudo systemctl restart pal-server
# 关闭幻兽帕鲁的服务
sudo systemctl stop pal-server
# 查询幻兽帕鲁服务的状态
sudo systemctl status pal-server
~~~

#### 强制更新

~~~
wget -O - https://raw.githubusercontent.com/zzqqw/palworld-install/main/sh/update_restart.sh|sh
~~~

#### 开放端口8211

幻兽帕鲁默认使用8211端口进行通信，进入服务商放通8211端口，协议UDP

#### [安装面板](https://github.com/zzqqw/palworld-install/tree/main/dashboard)

~~~
sudo apt install -y python3 python3-pip
sudo -u steam git clone https://github.com/zzqqw/palworld-install.git ~steam/palworld
pip install ~steam/palworld/dashboard/requirements.txt
python3 ~steam/palworld/dashboard/main.py 
~~~

#### 配置项

1、复制并执行以下命令为配置文件增加权限，避免后续步骤中由于权限问题导致无法编辑。

~~~
sudo chmod 777 /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
~~~

2、使用如下命令，将默认配置文件复制到幻兽帕鲁下的LinuxServer目录中：

默认情况下，PalWorldSettings.ini文件是空的，手动配置的门槛很高，因此我们推荐在默认配置文件的基础上进行修改。

~~~
sudo cp /home/steam/Steam/steamapps/common/PalServer/DefaultPalWorldSettings.ini /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
~~~

3、使用如下命令打开游戏参数的配置文件：PalWorldSettings.ini。

~~~
sudo vim /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
~~~

#### 备份数据

~~~
tar -cvf backup_saved.tar /home/steam/Steam/steamapps/common/PalServer/Pal/Saved
~~~

## 服务器优化

### 配置zram提高系统内存使用率，减少物理磁盘读写

~~~
sudo apt update -y
sudo apt-get install zram-config -y
sudo systemctl start zram-config.service
~~~

### 配置Swap

~~~
//创建一个swap文件
sudo fallocate -l 8G /swapfile
//设置文件权限
sudo chmod 600 /swapfile
//将文件格式化为swap格式
sudo mkswap /swapfile
//启用swap文件
sudo swapon /swapfile
//设置永久使用swap文件
echo /swapfile   none    swap    sw    0   0 >> /etc/fstab
//重新加载fstab文件
sudo swapon --all
//验证swap设置是否成功
swapon --show
~~~

## 常用脚本

### 监控内存占用并在占用比例达到 90% 时自动重启

~~~
cd ~
wget https://raw.githubusercontent.com/zzqqw/palworld-install/main/sh/auto_restart.sh
* * * * * /bin/bash ~/auto_restart.sh > /dev/null 2>&1
~~~

### 更新palworld服务器并完成重启

~~~
wget -O - https://raw.githubusercontent.com/zzqqw/palworld-install/main/sh/update_restart.sh|sh
~~~

