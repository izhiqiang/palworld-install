#!/bin/bash

set -e

if [[ -n $FORCE_UPDATE ]] && [[ $FORCE_UPDATE == "true" ]]; then
    /usr/games/steamcmd +login anonymous +app_update 2394010 validate +quit
fi

if [[ ! -f /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini ]]; then
    sudo mkdir -p /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/
    sudo cp /home/steam/Steam/steamapps/common/PalServer/DefaultPalWorldSettings.ini /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
    if [[ -n $SERVER_NAME ]]; then
        sudo sed -i "s^ServerName=\"Default Palworld Server\"^ServerName=\"$SERVER_NAME\"^g" /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
    fi
    if [[ -n $SERVER_DESC ]]; then
        sudo sed -i "s^ServerDescription=\"\"^ServerDescription=\"$SERVER_DESC\"^g" /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
    fi
    if [[ -n $ADMIN_PASSWORD ]]; then
        sudo sed -i "s^AdminPassword=\"\"^AdminPassword=\"$ADMIN_PASSWORD\"^g" /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
    fi
    if [[ -n $SERVER_PASSWORD ]]; then
        sudo sed -i "s^ServerPassword=\"\"^ServerPassword=\"$SERVER_PASSWORD\"^g" /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
    fi
    if [[ -n $RCON_ENABLED ]] && [[ $RCON_ENABLED == "true" ]]; then
        sudo sed -i "s^RCONEnabled=False^RCONEnabled=True^g" /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
    fi
    if [[ -n $RCON_PORT ]]; then
        sudo sed -i "s^RCONPort=25575^RCONPort=$RCON_PORT^g" /home/steam/Steam/steamapps/common/PalServer/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini
    fi
fi

sudo chmod 777 /home/steam/Steam/steamapps/common/PalServer/Pal/Saved
sudo chown -R steam:steam /home/steam/Steam/steamapps/common/PalServer/Pal/Saved

/home/steam/Steam/steamapps/common/PalServer/PalServer.sh port="$PORT" "$CLI_ARGS"