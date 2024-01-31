#!/bin/bash

set -e
set -u

version=$(curl --silent "https://api.steamcmd.net/v1/info/2394010" | jq '.data."2394010".depots.branches.public.buildid' -r)
currentversion=$(cat currentversion)
echo "currentversion:$currentversion version:$version"

# 判断版本号是否相同 如果相同就exit
if [[ "$currentversion" == "$version" ]]; then
    exit
fi

echo "Submit Docker Image"
# 登录仓库
docker login -u $DOCKER_USER -p $DOCKER_PWD
# 构建仓库
docker build -f Dockerfile.base -t zhiqiangwang/palworld-server:base  .
# 发布仓库
echo "Release Docker Version: " $version
docker push zhiqiangwang/palworld-server:base

echo "Submit the latest code"
# 更新代码
echo "$version" >currentversion
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add currentversion
git commit -a -m "Auto Update to buildid: $version"
git push origin main