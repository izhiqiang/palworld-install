#!/bin/bash

if [ "$(whoami)" = "root" ]; then
  echo "Error: Running as root user is not allowed" >&2
  exit 1
fi

steam_user=$(whoami)

echo "The current user being used is $steam_user"

echo "Installing SteamCMD..."
sudo add-apt-repository multiverse -y
sudo dpkg --add-architecture i386
sudo apt update -y
sudo apt-get remove needrestart -y

echo steam steam/license note '' | sudo debconf-set-selections
echo steam steam/question select "I AGREE" | sudo debconf-set-selections
sudo apt install steamcmd -y

steam_user_path=~steam
steamcmd_path=$(which steamcmd)

if [ -z "$steamcmd_path" ]; then
    echo "Error: Install SteamCMD failed"
    exit 1
else
    echo "Install SteamCMD successfully"
fi

sudo -u $steam_user mkdir -p $steam_user_path/.steam/sdk64/
echo "Downloading palServer..."
sudo -u $steam_user $steamcmd_path +login anonymous +app_update 1007 validate +quit
sudo -u $steam_user $steamcmd_path +login anonymous +app_update 2394010 validate +quit

sudo cp $steam_user_path/Steam/steamapps/common/Steamworks\ SDK\ Redist/linux64/steamclient.so $steam_user_path/.steam/sdk64/

systemd_unit=pal-server
cat <<EOF > $systemd_unit.service
[Unit]
Description=$systemd_unit.service

[Service]
Type=simple
User=$steam_user
Restart=on-failure
RestartSec=30s
ExecStart=$steam_user_path/Steam/steamapps/common/PalServer/PalServer.sh -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS

[Install]
WantedBy=multi-user.target
EOF

sudo mv $systemd_unit.service /usr/lib/systemd/system/
echo "Starting palServer..."
sudo systemctl enable $systemd_unit
sudo systemctl restart $systemd_unit
sudo systemctl -l --no-pager status $systemd_unit

if systemctl --quiet is-active "$systemd_unit"
then
    echo -e "\nPalServer is running successfully, enjoy!"
else
    echo -e "\nThere were some problems with the installation, please check the log."
fi

echo "Installing zram..."
sudo apt-get install zram-config -y

sleep 1
sudo systemctl start zram-config.service
