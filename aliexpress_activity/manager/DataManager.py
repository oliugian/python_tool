# -*- coding: utf-8 -*-
import os
from model.User import *
from LogManager import *
class DataManager(object):

    def __init__(self,init = True):
        if init:
            self.initData()
    def initData(self):
        self.config_path = os.path.abspath("./config")
        self.dataPath = os.path.abspath("./data")
        self.look_and_look_urls_path = os.path.join(self.config_path, "look_and_look_urls.txt")

        self.userDataPath = os.path.join(self.dataPath,"ipUserData.txt")
        self.proxyIpPath = os.path.join(self.dataPath,"proxyIp.txt")
        self.userNamePath = os.path.join(self.dataPath, "userName.txt")

        self.allIPUser = {}
        self.allProxyIp = []
        self.look_and_look_urls = []
        self.userNames = []

        log_info("###################### Start to init data #################")
        self.readFromFile(self.userDataPath,"ipUserData")
        self.readFromFile(self.proxyIpPath,"proxyIp")
        self.readFromFile(self.userNamePath,"userName")
        self.readFromFile(self.look_and_look_urls_path, "url")
        log_info("###################### Init data finish ###################")


    def readFromFile(self,dataPath,dataType):
        f = open(dataPath, 'r')
        for line in f.readlines():
            line = str(line).strip("\n")
            if dataType == "url":
                self.look_and_look_urls.append(line)
            elif dataType == "userName":
                self.userNames.append(line)
            elif dataType == "proxyIp":
                self.allProxyIp.append(line)
            elif dataType == "ipUserData":
                ip_user_temp = line.split("|")
                if len(ip_user_temp) != 3:
                    self.allIPUser[ip_user_temp[0]] = None
                else:
                    self.allIPUser[ip_user_temp[0]] = User(ip_user_temp[1],ip_user_temp[2])
        if dataType == "ipUserData":
            log_info("Init userData , get "+str(len(self.allIPUser))+" users.")
        elif dataType == "userName":
            log_info("Init userName finish, get "+str(len(self.userNames))+" user names.")
        elif dataType == "proxyIp":
            log_info("Init proxyIp finish, get "+str(len(self.allProxyIp))+" proxy ips.")
        elif dataType == "url":
            log_info("Init product look and look url, get " + str(len(self.look_and_look_urls)) + " urls.")
        f.close()

    def sortedDictValues(self,adict):
        keys = adict.keys()
        keys.sort()
        return [dict[key] for key in keys]

    def updataIpUser(self,all_ip_user):
        f = open(self.userDataPath, 'w')
        all_ip_user = sorted(all_ip_user.iteritems(), key=lambda asd: asd[0])
        for enty in all_ip_user:
            user_tmp = enty[1]
            if user_tmp is not None and user_tmp != "":
                f.write(str(enty[0]).strip("\n")+"|"+user_tmp.email+"|"+user_tmp.passwd+"\n")
        f.close()