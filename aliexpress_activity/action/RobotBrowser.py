# -*- coding: utf-8 -*-
# @Author: LC
# @Date:   2016-08-15 22:34:08
# @Last modified by:   LC
# @Last Modified time: 2017-03-23 17:25:42
# @Email: liangchaowu5@gmail.com

###################################################################################
# Function: simulate some actions manipulated by humans with gui, including:
# 1. sign up and sign in
# 2. search keywords and visit target product
# 3. add product to cart
###################################################################################




import random
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import pickle
from selenium.webdriver.common.action_chains import ActionChains
from manager.TimeManager import *
from commonException.LoginException import *
from commonException.AuthException import *
from selenium.common.exceptions import UnexpectedAlertPresentException

class RobotBrowser:
    def __init__(self, proxy=None):
        """init the webdriver by setting the proxy and user-agent

        Args:
            proxy (str): proxy in the form of ip:port
        """
        self.aliexpress_index = r'https://www.aliexpress.com/'

        #self.libPath = os.path.abspath("./lib/geckodriver64.exe")
        self.libPath = os.path.abspath("./lib/chromedriver.exe")
        self.cookiePath = os.path.abspath("./cookie/cookies.pickle")
        self.discount_url_for_check = r"https://mypromotion.aliexpress.com/store/storediscount/create.htm"
        #self.driver = webdriver.Firefox(executable_path=self.libPath)

        self.driver = webdriver.Chrome(executable_path=self.libPath)

    def checkIsLogin(self):
        try:
            self.openUrl(self.discount_url_for_check)
            self.driver.find_element_by_id("alibaba-login-box")
            return False
        except Exception,e:
            return True
    def waitForContent(self, content, timeCount=20):
        result = None
        count = 0
        while True:
            try:
                result = self.driver
            except NoSuchElementException, e:
                pass
            if result:
                log_info("Load Finish.")
                break
            waitSeconds(3)
            count = count + 1
            if count > timeCount:
                raise TimeoutException("wait for load Finish time out.")
            log_info("Not load Finish, wait " + str(3 * count) + " seconds. check id :" + content)

    def waitUrlCorrect(self, content, timeCount=10):
        count = 0
        while True:
            current_url = self.driver.current_url
            if content in current_url:
                log_info("url correct.")
                break
            waitSeconds(3)
            count = count + 1
            if count > timeCount:
                raise TimeoutException("wait for url correct time out.")
            log_info("Url wrong, wait " + str(3 * count) + " seconds. check content :" + content)

    def waitForLoginFinish(self, checkId, timeCount=10):
        result = None
        count = 0
        while True:
            try:
                result = self.driver.find_element_by_id(checkId)
            except NoSuchElementException, e:
                pass
            if result != None:
                break
            ##need verifying
            try:
                result = self.driver.find_element_by_id("cvf-page-content")
                raise LoginException("this account need verifying")
            except NoSuchElementException, e:
                pass
            try:
                result = self.driver.find_element_by_id("auth-error-message-box")
                raise LoginException("this account auth-error")
            except NoSuchElementException, e:
                pass
            ##need auth
            try:
                result = self.driver.find_element_by_id("auth-captcha-guess")
                raise AuthException("this ip need auth")
            except NoSuchElementException, e:
                pass
            try:
                result = self.driver.find_element_by_id("captchacharacters")
                raise AuthException("this ip need auth")
            except NoSuchElementException, e:
                pass
            waitSeconds(3)
            count = count + 1
            if count > timeCount:
                raise TimeoutException("wait for load Finish time out.")

    def waitForReloadFinish(self, checkId, timeCount=10):
        result = None
        count = 0
        while True:
            try:
                result = self.driver.find_element_by_id(checkId)
                break
            except NoSuchElementException, e:
                pass
            waitSeconds(3)
            count = count + 1
            if count > timeCount:
                raise TimeoutException("wait for load Finish time out.")

    def move_slide(self):

        dragger = self.driver.find_element_by_id("nc_1_n1z")
        action = ActionChains(self.driver)
        action.click_and_hold(dragger).perform()
        for index in range(250):
            try:
                action.move_by_offset(2, 0).perform()  # 平行移动鼠标
            except UnexpectedAlertPresentException:
                break
            action.reset_actions()
            time.sleep(0.1)

        # submit_b = self.driver.find_element_by_name("fm-login-submit")
        # submit_b.click()

    def set_cookies(self):
        if os.path.exists(self.cookiePath):
            cookies = pickle.load(open(self.cookiePath, "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)


    def sign_in(self, username,passwd, sign_in_url=r'https://login.aliexpress.com/'):
        self.openUrl(sign_in_url,"headerReg")
        self.driver.switch_to_frame("alibaba-login-box")
        inputElement = self.driver.find_element_by_id("fm-login-id")
        inputElement.send_keys(username)
        waitRandomSecons(3)
        # inputElement = self.driver.find_element_by_id("fm-login-password")
        # waitRandomSecons(3)
        # inputElement.send_keys(passwd)
        # waitSeconds(20)
        print("input your username and password in Firefox and hit Submit")
        raw_input("Hit Enter here if you have summited the form: ")
        self.openUrl(self.aliexpress_index)
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open(self.cookiePath, "wb"))

        # try:
        #     submit_b = self.driver.find_element_by_name("fm-login-submit")
        #     submit_b.click()
        # except Exception,e:
        #     self.driver.refresh()
        #     self.driver.switch_to_frame("alibaba-login-box")
        #     inputElement = self.driver.find_element_by_id("fm-login-id")
        #     inputElement.send_keys(username)
        #     waitSeconds(3)
        #     inputElement = self.driver.find_element_by_id("fm-login-password")
        #     inputElement.send_keys(passwd)
        #     submit_b = self.driver.find_element_by_name("fm-login-submit")
        #     submit_b.click()
        # waitSeconds(3)
        # log_info("user " + username + " login success.")

    def openUrl(self, urlPath, checkId=None):
        try:
            self.driver.get(urlPath)
        except Exception, e:
            pass
        finally:
            if checkId != None:
                self.waitForReloadFinish(checkId)
    def createStoreDiscount(self,task,discount_url="https://mypromotion.aliexpress.com/store/storediscount/create.htm"):
        self.openUrl(discount_url)
        inputElement = self.driver.find_element_by_id("promotion-title")
        inputElement.send_keys(task.name)
        inputElement = self.driver.find_element_by_id("start-date")
        self.driver.execute_script("arguments[0].value='"+str(task.begin_date)+"'",inputElement)
        inputElement = self.driver.find_element_by_id("start-date-time")
        self.driver.execute_script("arguments[0][" + str(task.begin_time) + "].selected=true", inputElement)
        inputElement = self.driver.find_element_by_id("end-date")
        self.driver.execute_script("arguments[0].value='" + str(task.end_date) + "'", inputElement)
        inputElement = self.driver.find_element_by_id("end-date-time")
        self.driver.execute_script("arguments[0][" + str(task.end_time) + "].selected=true", inputElement)
        tables_row = self.driver.find_element_by_id("product-group-list").find_elements_by_tag_name("tr")
        all_row = len(tables_row)
        row = 0
        while row < all_row:
            table_cols = tables_row[row].find_elements_by_tag_name("td")
            group_name = table_cols[0].text
            # group_name = table_cols[0].find_element_by_tag_name("a").text
            if group_name.find("ther") != -1:
                discount_moble = 6
                discount_pc = 5
            else:
                d_temp = group_name.split("%")
                discount_moble = int(d_temp[0])
                if discount_moble > 5:
                    discount_pc = discount_moble-1
                else:
                    discount_pc = discount_moble
                    discount_moble = discount_moble+1

            pc_tmp = table_cols[1].find_element_by_tag_name("input")
            pc_tmp.send_keys(discount_pc)
            mb_tmp = table_cols[2].find_element_by_tag_name("input")
            mb_tmp.send_keys(discount_moble)
            row = row + 2
        submit_btn = self.driver.find_element_by_id("create-btn")
        submit_btn.click()
        waitSeconds(5)
        # inputElements = self.driver.find_elements_by_xpath("//input[@class='pc-discount']")
        # count = 1
        # for discount in inputElements:
        #     key = "discount_"+str(count)
        #     discount.send_keys(task.getDiscount(key))
        #     count = count + 1


    def exit_driver(self):
        """exit the webdriver"""
        try:
            self.driver.quit()
        except Exception, e:
            print 'Error while exiting the web driver\n%s' % e.message

if __name__ == '__main__':
    robot = RobotBrowser()
    username=r""
    passwd=r""
    robot.sign_in(username,passwd)
    robot.openUrl(robot.aliexpress_index, "top-lighthouse")
    robot.set_cookies()
    robot.openUrl(robot.aliexpress_index, "top-lighthouse")
    robot.createStoreDiscount()



