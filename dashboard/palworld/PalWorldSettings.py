import json
import logging
import os
import re
import time
from shutil import copyfile

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
        self.palWorldSettingsIniFile = os.path.join(os.environ.get("PalServerPath"), "Pal", "Saved", "Config",
                                                    "LinuxServer", palWorldSettingsINIFile)

        self.formjson = os.environ.get("FormJSONPalWorldSettings")

    # 读取form数据
    def readForm(self):
        if not os.path.exists(self.formjson):
            logging.error("Unable to find %s file", self.formjson)
            return None
        with open(self.formjson, 'r') as file:
            return json.load(file)

    # 渲染前端模版参数
    def RenderForm(self):
        form = self.readForm()
        optionSettings = self.ReadOptionSettings()
        if form is not None:
            if optionSettings is not None:
                for key, value in optionSettings.items():
                    if key in form:
                        form[key]["default"] = value
                    else:
                        logging.warning("The `%s` data type is not defined in the %s file", key, self.formjson)
        return form

    # 读取配置项
    def ReadOptionSettings(self):
        if not os.path.exists(self.palWorldSettingsIniFile):
            logging.error("Unable to find %s file", self.formjson)
            return None
        with open(self.palWorldSettingsIniFile, 'r', encoding='utf-8') as file:
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
        if not os.path.exists(self.palWorldSettingsIniFile):
            logging.error("Unable to find %s file", self.formjson)
            return None
        form = self.RenderForm()
        if form is None:
            return None
        bakConfigFile = self.palWorldSettingsIniFile + "." + format(int(time.time()))
        logging.warning("Back up configuration files to %s", bakConfigFile)
        copyfile(self.palWorldSettingsIniFile, bakConfigFile)
        with open(self.palWorldSettingsIniFile, 'w', encoding='utf-8') as file:
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
        restartcmd = os.environ.get("RestartCommand")
        if restartcmd is not None:
            if restartcmd != "":
                logging.warning("Restarting server %s log %s", restartcmd, os.system(restartcmd))
