import logging
import os
import re
import time
from shutil import copyfile

import util


class PalWorldSettings(object):
    palWorldSettingsFileName = "PalWorldSettings.ini"

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
                                                     "LinuxServer", self.palWorldSettingsFileName)
        else:
            self.palWorldSettingsFile = "./" + self.palWorldSettingsFileName

        # self.palWorldSettingsFile = "./" + self.palWorldSettingsFileName

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
        return util.readJSONFile(self.formjson)

    def readerSubmitButtonTitle(self) -> str:
        env = util.osnvironget("DASHBOARD_CONFIG_BUTTON_TYPE")
        if env is None:
            return "下载配置"
        else:
            return "提交配置"

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

    def configStr(self, optionSettings: dict) -> str:
        if not os.path.exists(self.palWorldSettingsFile):
            logging.error("Unable to find %s file", self.palWorldSettingsFile)
            raise FileNotFoundError
        form = self.readFormJSON()
        # 配置文件内容开始
        content = "[/Script/Pal.PalGameWorldSettings]\n"
        content += "OptionSettings=("
        for key, value in optionSettings.items():
            if key in form:
                if key not in self.strList:
                    content += f"{key}={value},"

                else:
                    content += f"{key}=\"{value}\","
            else:
                logging.warning("Skipping configuration %s when writing files", key)
        return content[:-1] + ")"

    # 写入配置文件
    def writeConfig(self, configStr: str):
        bakConfigFile = self.palWorldSettingsFile + "." + format(int(time.time()))
        logging.warning("Back up configuration files to %s", bakConfigFile)
        copyfile(self.palWorldSettingsFile, bakConfigFile)
        # 将配置文件内容写入到文件中
        util.writeFile(self.palWorldSettingsFile, configStr)
        # 重启服务
        if self.restartCommand is not None:
            logging.warning("Restarting server %s log %s", self.restartCommand, os.system(self.restartCommand))
