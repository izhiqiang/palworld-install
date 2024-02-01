import json
import logging
import os
import re
import time
from shutil import copyfile

import util

palWorldSettingsINIFile = "PalWorldSettings.ini"


class PalWorldSettings(object):
    def __init__(self):
        self.strList = [
            "ServerName",
            "ServerDescription",
            "AdminPassword",
            "ServerPassword",
            "PublicIP",
            "Region",
            "BanListURL"
        ]
        logging.debug("Fields that need to be processed as strings when writing files %s", self.strList)

        # palworld 游戏目录（然后凭借完整配置文件路径）
        palServerPath = util.osnvironget("PALSERVERPATH")
        if palServerPath is not None:
            self.palWorldSettingsFile = os.path.join(palServerPath, "Pal", "Saved", "Config",
                                                     "LinuxServer", palWorldSettingsINIFile)
        else:
            self.palWorldSettingsFile = "./" + palWorldSettingsINIFile

        # self.palWorldSettingsFile = "./" + palWorldSettingsINIFile

        # 前端渲染form 表单json
        formjson = util.osnvironget("FORMJSON_PALWORLDSETTINGS")
        if formjson is not None:
            self.formjson = formjson
        else:
            self.formjson = "./form/PalWorldSettings.json"

        # 重启palworld服务器命令
        self.restartCommand = util.osnvironget("RESTARTPALSERVER_COMMAND")

    # 读取form数据
    def readFormJSON(self):
        if not os.path.exists(self.formjson):
            logging.error("Unable to find %s file", self.formjson)
            raise FileNotFoundError
        with open(self.formjson, 'r') as file:
            return json.load(file)

    # 渲染前端模版参数
    def RenderForm(self):
        form = self.readFormJSON()
        optionSettings = self.ReadOptionSettings()
        if optionSettings is not None:
            for key, value in optionSettings.items():
                if key in form:
                    form[key]["default"] = value
                else:
                    logging.warning("The `%s` data type is not defined in the %s file", key, self.formjson)
        return form

    # 读取配置项
    def ReadOptionSettings(self):
        if not os.path.exists(self.palWorldSettingsFile):
            logging.error("Unable to find %s file", self.formjson)
            raise FileNotFoundError
        with open(self.palWorldSettingsFile, 'r', encoding='utf-8') as file:
            content = file.read()
            options = {}
            pattern = r"\(([\w\W]*?)\)"
            matches = re.search(pattern, content).group(1).split(",")
            matches = [match.split("=") for match in matches]
            matches = [(name, value.strip('\"')) for name, value in matches]
            for match in matches:
                option, value = match
                options.update({option: value})
            return options

    # 写入配置文件
    def WriteConfig(self, optionSettings):
        if not os.path.exists(self.palWorldSettingsFile):
            logging.error("Unable to find %s file", self.palWorldSettingsFile)
            raise FileNotFoundError
        form = self.readFormJSON()
        bakConfigFile = self.palWorldSettingsFile + "." + format(int(time.time()))
        logging.warning("Back up configuration files to %s", bakConfigFile)
        copyfile(self.palWorldSettingsFile, bakConfigFile)
        with open(self.palWorldSettingsFile, 'w', encoding='utf-8') as file:
            file.write("[/Script/Pal.PalGameWorldSettings]\n")
            file.write("OptionSettings=(")
            for key, value in optionSettings.items():
                if key in form:
                    if key not in self.strList:
                        file.write(f"{key}={value},")
                    else:
                        file.write(f"{key}=\"{value}\",")
                else:
                    logging.warning("Skipping configuration %s when writing files", key)
            file.seek(file.tell() - 1, 0)
            file.write(")")
        # 重启服务
        if self.restartCommand is not None:
            logging.warning("Restarting server %s log %s", self.restartCommand, os.system(self.restartCommand))
