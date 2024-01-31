Can help you set up Palworld on the server

## Internationalization Doc

- [Chinese documents](./README.md)
- [English document](./README.EN.md)

# Server configuration recommendations


| Number of people | Recommended configuration |
| ---------------- | ------------------------- |
| 4～8             | 4-core 16G                |
| 10～20           | 8-core 32G                |
| 16～24           | 16 core 32G               |
| 32人             | 16 core 64G               |

## How to obtain

### docker

~~~
git clone https://github.com/zzqqw/palworld-install.git
cd palworld-install
//Basic version
docker-compose -f docker-compose.base.yml up -d
//Carrying panels
docker-compose -f docker-compose.yml up -d
~~~

### Script installation

> Server package configuration: Taking a 4-core CPU and 16GB of memory as an example (usually able to accommodate 6-8 people online simultaneously)
>
> Operating System: Ubuntu 22.04 LTS

~~~
wget -O - https://raw.githubusercontent.com/zzqqw/palworld-install/main/install.sh|sh
~~~

#### Related commands

~~~
sudo systemctl start pal-server
sudo systemctl restart pal-server
sudo systemctl stop pal-server
sudo systemctl status pal-server
~~~

#### configuration

~~~
sudo chmod 777 /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
sudo cp /home/steam/Steam/steamapps/common/PalServer/DefaultPalWorldSettings.ini /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
sudo vim /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
~~~

#### Force updates

~~~
sudo -u steam /home/steam/Steam +login anonymous +app_update 2394010 validate +quit
sudo systemctl restart pal-server
~~~

#### Data backup

~~~
tar -cvf backup_saved.tar /home/steam/Steam/steamapps/common/PalServer/Pal/Saved
~~~

## Server optimization

### Configure zram 

> Configure zram to improve system memory usage and reduce physical disk read and write

~~~
sudo apt update -y
sudo apt-get install zram-config -y
sudo systemctl start zram-config.service
~~~

### Configure Swap

~~~
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo /swapfile   none    swap    sw    0   0 >> /etc/fstab
sudo swapon --all
swapon --show
~~~

## Common scripts

### automatic restart

~~~
cd ~
wget https://raw.githubusercontent.com/zzqqw/palworld-install/main/auto_restart.sh
* * * * * /bin/bash ~/auto_restart.sh > /dev/null 2>&1
~~~