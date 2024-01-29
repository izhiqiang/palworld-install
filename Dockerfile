FROM ubuntu:22.04

RUN apt update

# 安装需要的依赖
RUN apt-get update && apt-get install -y sudo software-properties-common

# 添加steam用户
RUN useradd -m -s /bin/bash steam && \
    echo 'steam ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers


ENV CLI_ARGS="-useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS"
ENV PORT=8211
ENV SERVER_NAME="Default Palworld Server"
ENV SERVER_DESC="Default Palworld Server"
ENV ADMIN_PASSWORD=steam
ENV SERVER_PASSWORD=""
ENV RCON_ENABLED=false
ENV RCON_PORT=25575
ENV FORCE_UPDATE=false

# 切换到steam用户
USER steam
WORKDIR /home/steam
# 安装SteamCMD
RUN sudo echo steam steam/license note '' | sudo debconf-set-selections
RUN sudo echo steam steam/question select "I AGREE" | sudo debconf-set-selections
RUN sudo add-apt-repository multiverse && sudo dpkg --add-architecture i386 \
    && sudo apt-get update && sudo apt-get install -y steamcmd

RUN mkdir -p ~/.steam/sdk64
RUN /usr/games/steamcmd +login anonymous +app_update 1007 validate +quit
RUN /usr/games/steamcmd +login anonymous +app_update 2394010 validate +quit

RUN sudo cp /home/steam/Steam/steamapps/common/Steamworks\ SDK\ Redist/linux64/steamclient.so /home/steam/.steam/sdk64/

EXPOSE ${PORT}/udp ${RCON_PORT}/tcp

COPY docker-entrypoint.sh /
RUN sudo chmod +x /docker-entrypoint.sh


RUN sudo apt-get clean && sudo rm -rf /var/lib/apt/lists/*
RUN sudo rm -rf /tmp/*

RUN mkdir -p /home/steam/Steam/steamapps/common/PalServer/Pal/Saved
RUN mkdir -p /home/steam/Steam/steamapps/common/PalServer/Pal/Content/Paks/MOD

VOLUME [ "/home/steam/Steam/steamapps/common/PalServer/Pal/Saved", "/home/steam/Steam/steamapps/common/PalServer/Pal/Content/Paks/MOD" ]

ENTRYPOINT [ "/docker-entrypoint.sh" ]