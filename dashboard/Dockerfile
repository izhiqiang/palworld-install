FROM ubuntu:22.04

RUN apt-get update && apt install -y python3-dev python3-pip

RUN mkdir -p /data

WORKDIR /data

ADD . .

RUN rm -rf .env
ENV PalServerPath=/home/steam/Steam/steamapps/common/PalServer/
ENV FormJSONPalWorldSettings=./form/PalWorldSettings.json
ENV BasicUser=zzqqw
ENV BasicPwd=123456

# 安装pip依赖
RUN pip3 install --no-cache-dir -r /data/requirements.txt

EXPOSE 8000

RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp/*

CMD python3 main.py