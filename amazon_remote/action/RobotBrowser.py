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



# import requests

import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

from commonException.LoginException import *
from commonException.AuthException import *
from manager.TimeManager import *
from model.User import *


class RobotBrowser:
    def __init__(self, proxy=None):
        """init the webdriver by setting the proxy and user-agent

        Args:
            proxy (str): proxy in the form of ip:port
        """
        self.amazon_index = r'https://www.amazon.com/'
        self.libPath = os.path.abspath("./lib/geckodriver64.exe")
        if proxy == None:
            self.driver = webdriver.Firefox(executable_path=self.libPath)
            # self.driver = webdriver.Chrome(executable_path=self.libPath)
            # self.driver = webdriver.PhantomJS(executable_path=self.libPath)
            self.proxy = ""
        else:
            self.proxy = proxy
            ip, port = proxy.split(':')
            profile = webdriver.FirefoxProfile()
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", ip)
            profile.set_preference("network.proxy.http_port", int(port))
            profile.set_preference("network.proxy.ssl", ip)
            profile.set_preference("network.proxy.ssl_port", int(port))
            profile.set_preference("browser.tabs.remote.autostart.2", False)

            profile.set_preference('permissions.default.image', 2)
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

            # for auth
            # profile.add_extension(self.auth_proxy_path)
            # credentials = 'User-002:fcg1994'
            # credentials = b64encode(credentials.encode('ascii')).decode('utf-8')
            # profile.set_preference('extensions.closeproxyauth.authtoken', credentials)
            # profile.set_preference('permissions.default.image', 2)
            # profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
            # # save identify code
            # profile.set_preference('browser.download.folderList', 2)
            # profile.set_preference('browser.download.manager.showWhenStarting', False)
            # profile.set_preference('browser.download.dir','./verifyCode/images')
            # profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'image/jpeg')

            # set user_agent
            # profile.set_preference("general.useragent.override", generate_user_agent())
            profile.update_preferences()
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % proxy)

            proxy_driver = webdriver.Proxy()
            proxy_driver.proxy_type = ProxyType.MANUAL
            proxy_driver.http_proxy = proxy
            # self.driver = webdriver.PhantomJS(self.libPath)
            # proxy_driver.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
            # self.driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
            self.driver = webdriver.Firefox(executable_path=self.libPath, firefox_profile=profile)
            # self.driver = webdriver.Chrome(executable_path=self.libPath,chrome_options=chrome_options)

            log_info('current proxy: %s' % proxy)
            # self.driver.set_page_load_timeout(60)

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
            try:
                result = self.driver.find_element_by_id("captchacharacters")
                raise AuthException("this ip need auth")
            except NoSuchElementException, e:
                pass
            waitSeconds(3)
            count = count + 1
            if count > timeCount:
                raise TimeoutException("wait for load Finish time out.")

    def waitForAddingShoppingCardFinish(self, timeCount=10):
        result = None
        count = 0
        while True:
            try:
                self.driver.find_element_by_id("huc-v2-order-row-container")
                break
            except NoSuchElementException, e:
                pass
            try:
                self.driver.find_element_by_id("captchacharacters")
                raise AuthException("this ip need auth")
            except NoSuchElementException, e:
                pass
            try:
                result_target = self.driver.find_element_by_id("siNoCoverage-announce")
                result_target.click()
            except Exception, e:
                pass

            try:
                result_target = self.driver.find_element_by_id("sbbop-no-button")
                self.driver.execute_script("arguments[0].click();", result_target)
            except Exception, e:
                pass
            try:
                result_target = self.driver.find_element_by_xpath("//span[@id='sbbop-no-button']/span")
                self.driver.execute_script("arguments[0].click();", result_target)
            except Exception, e:
                pass
            try:
                result_target = self.driver.find_element_by_xpath("//span[@id='sbbop-no-button']/span/input")
                self.driver.execute_script("arguments[0].click();", result_target)
            except Exception, e:
                pass
            try:
                result_target = self.driver.find_element_by_xpath("//span[@id='sbbop-no-button']/span/a")
                self.driver.execute_script("arguments[0].click();", result_target)
            except Exception, e:
                pass
            waitSeconds(3)
            count = count + 1
            if count > timeCount:
                raise TimeoutException("wait for adding shopping cart Finish time out.")
                # log_info("Not load Finish, wait "+str(3*count)+" seconds. check id :"+checkId)

    def waitForAddingWishFinish(self, checkId, chekId2=None, timeCount=10):
        result = None
        result2 = None
        count = 0
        while True:
            try:
                result = self.driver.find_element_by_id(checkId)
            except NoSuchElementException, e:
                result = None
                pass
            if chekId2 != None:
                try:
                    result2 = self.driver.find_element_by_id(chekId2)
                except NoSuchElementException, e:
                    result2 = None
            if result != None and result.is_displayed():
                log_info("Display Finish.")
                break
            if result2 != None:
                log_info("Display Finish.")
                break
            if result2 is None:
                try:
                    self.driver.find_element_by_id("WLNEW_newwl_section").click()
                    waitRandomSecons()
                    self.driver.find_element_by_id("WLNEW_submit").click()
                    waitRandomSecons()
                    break
                except Exception, e:
                    pass

            try:
                target = self.driver.find_element_by_xpath("//input[@alt='Create a List']")
                target.click()
            except Exception, e:
                pass
            try:
                target = self.driver.find_element_by_id("WLHUC_result_success")
                break
            except Exception, e:
                pass
            waitSeconds(3)
            count = count + 1
            if count > timeCount:
                raise TimeoutException("wait for display Finish time out.")
            log_info("Not display Finish, wait " + str(3 * count) + " seconds. check id :" + checkId)

    def sign_in(self, user, sign_in_url=r'https://www.amazon.com/gp/sign-in.html'):
        self.openUrl(self.amazon_index, "nav-link-accountList")
        self.driver.find_element_by_id("nav-link-accountList").click()
        self.waitForReloadFinish("ap_email")
        inputElement = self.driver.find_element_by_name("email")
        inputElement.send_keys(user.email)
        waitRandomSecons()
        inputElement = self.driver.find_element_by_name("password")
        inputElement.send_keys(user.passwd)
        waitRandomSecons()
        inputElement.submit()
        self.waitForLoginFinish("nav-link-accountList")
        waitSeconds()
        log_info("user " + user.email + " login success.")

    def scroll_to_target(self, check_id, is_buttom=True, scroll_time=5, start_target=None, ignore_final=True):
        self.waitForReloadFinish(check_id)
        target_element = self.driver.find_element_by_id(check_id)
        location_heigh = target_element.location['y']
        next_scroll = 0
        if start_target is not None:
            next_scroll = self.driver.find_element_by_id(start_target).location['y']
        tmp_average = (location_heigh - next_scroll) / scroll_time

        for i in range(scroll_time):
            waitRandomSecons()
            self.driver.execute_script("window.scrollTo(0,%s)" % next_scroll)
            next_scroll = next_scroll + tmp_average
        if ignore_final:
            if is_buttom:
                self.driver.execute_script("arguments[0].scrollIntoView(false);", target_element)
            else:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", target_element)

    def show_all_result(self):
        try:
            continue_link = self.driver.find_element_by_link_text('Show all results')
            continue_link.click()
            waitSeconds()
        except Exception, e:
            pass
        try:
            target = self.driver.find_element_by_xpath("//div[@id='centerBelowPlus']/div/div/span/a")
            target.click()
            waitRandomSecons()
        except Exception, e:
            pass

    def search_keywords(self, words, asin_id, max_page=20, product_type=None):
        """type in keywords to search on the index page of amazon

        Args:
            words (str): words used to search items, seperated by space
        """
        self.openUrl(self.amazon_index, "twotabsearchtextbox")

        if product_type is not None and product_type != "":
            actions = ActionChains(self.driver)
            searchDropDown = self.driver.find_element_by_id('searchDropdownBox')
            actions.move_to_element(searchDropDown)
            actions.click_and_hold(searchDropDown)
            actions.perform()
            waitRandomSecons()
            select = Select(searchDropDown)
            select.select_by_visible_text(product_type)
        inputElement = self.driver.find_element_by_id('twotabsearchtextbox')
        inputElement.send_keys(words)
        waitRandomSecons()
        inputElement.submit()
        waitRandomSecons()
        self.show_all_result()
        # time.sleep(5000)

        self.waitForReloadFinish("s-results-list-atf")
        waitRandomSecons()
        page_index = 1
        wait_product_id = "s-results-list-atf"
        while True:
            try:
                self.waitForReloadFinish(wait_product_id)
                target = self.driver.find_element_by_xpath(
                    "//ul[@id='s-results-list-atf']/li[@data-asin='%s']" % asin_id)
                # target = self.driver.find_element_by_xpath("//ul[@id='s-results-list-atf']")
                target = target.find_element_by_class_name("s-access-detail-page")
            except NoSuchElementException, e:
                target = None
            if target is not None:
                log_info("find product " + asin_id + " in page " + str(page_index))
                waitSeconds(3)
                target_url = target.get_attribute("href")
                self.openUrl(target_url, "add-to-cart-button")
                break
            else:
                if page_index == max_page:
                    raise Exception("product %s not found within %s" % asin_id, max_page)
                page_index = page_index + 1
                self.waitForReloadFinish("pagnNextLink")
                next_page = self.driver.find_element_by_id("pagnNextLink")
                self.scroll_to_target("pagnNextLink")
                self.driver.execute_script("arguments[0].click();", next_page)
                waitRandomSecons()
                self.waitUrlCorrect("page=%s" % page_index)
                log_info("go to next page.")

    def openUrl(self, urlPath, checkId=None):
        try:
            self.driver.get(urlPath)
        except Exception, e:
            pass
        finally:
            if checkId != None:
                self.waitForReloadFinish(checkId)

    def check_some_alt_images(self):
        alt_images = self.driver.find_element_by_id("altImages")
        alt_images = alt_images.find_elements_by_class_name("imageThumbnail")
        all_count = len(alt_images)
        check_count = all_count / 2
        for i in range(check_count):
            index_tmp = random.randint(0, all_count - 1)
            alt_images[index_tmp].click()
            waitSeconds(3)

    def comment_like(self, like_count=3):
        self.scroll_to_target("cm-cr-dp-review-list", False)
        all_comments = self.driver.find_elements_by_xpath("//div[@id='cm-cr-dp-review-list']/div")
        tmp_count = 0
        for i in range(len(all_comments)):
            point = all_comments[i].find_element_by_xpath(".//div/div/a/i[@data-hook='review-star-rating']")
            if 'a-star-5' in point.get_attribute("class"):
                if tmp_count < like_count:
                    vote_yes = all_comments[i].find_element_by_link_text('Yes')
                    if vote_yes == None:
                        continue
                    waitRandomSecons()
                    vote_yes.click()
                    tmp_count = tmp_count + 1

    def view_qa(self, start_id="altImages"):
        # self.scroll_to_target("ask_lazy_load_div", False, 5, start_id)
        # waitRandomSecons()
        view_type = random.randint(0, 2)
        view_type = 0
        self.scroll_to_target("ask_lazy_load_div", scroll_time=3)
        qa_all = self.driver.find_element_by_id("ask_lazy_load_div")
        # open more qa
        if view_type == 0:
            try:
                see_more_qa = qa_all.find_element_by_class_name("askSeeMoreQuestionsLink")
                see_more_qa.click()
            except Exception, e:
                pass
            waitRandomSecons()
        elif view_type == 1:
            pass
            # all_top_ask = self.driver.find_elements_by_class_name("askWidgetSeeAllAnswersInline")
            # all_top_ask = self.driver.find_elements_by_css_selector("a.askWidgetSeeAllAnswersInline")
            # print len(all_top_ask)
            # target_ask = all_top_ask[random.randint(0, len(all_top_ask) - 1)]
            # self.driver.execute_script("arguments[0].click();", target_ask)

    def see_other_product(self):
        current_url = self.driver.current_url
        view_type = random.randint(0, 2)
        if view_type == 0:
            sp_detail = self.driver.find_element_by_id("sp_detail")
            all_sp = sp_detail.find_elements_by_class_name("sp_dpOffer")
            target_sp = all_sp[random.randint(0, len(all_sp) - 1)].find_element_by_xpath(".//a")

            self.driver.execute_script("arguments[0].click();", target_sp)
            waitRandomSecons()
            self.scroll_to_target("reviews-medley-footer", True, scroll_time=10, ignore_final=False)
            self.openUrl(current_url, "sp_detail")
        elif view_type == 1:
            sp_detail = self.driver.find_element_by_id("purchase-sims-feature")
            all_sp = sp_detail.find_elements_by_class_name("a-carousel-card")
            target_sp = all_sp[random.randint(0, len(all_sp) - 1)].find_element_by_xpath(".//div/a")
            self.driver.execute_script("arguments[0].click();", target_sp)
            waitRandomSecons()
            self.scroll_to_target("reviews-medley-footer", True, scroll_time=10, ignore_final=False)
            self.openUrl(current_url, "purchase-sims-feature")

    def view_bad_view(self):
        current_url = self.driver.current_url
        sp_detail = self.driver.find_element_by_id("histogramTable")
        target_sp = sp_detail.find_element_by_xpath(".//tbody/tr[@data-reftag='cm_cr_dp_d_hist_1']")
        target_sp = target_sp.find_element_by_tag_name("a")
        self.driver.execute_script("arguments[0].click();", target_sp)
        waitRandomSecons()
        self.scroll_to_target("navFooter", True, scroll_time=10, ignore_final=False)
        self.openUrl(current_url, "histogramTable")

    def select_color_target(self, select_id=None):
        if select_id is None or select_id == "":
            return
        current_url = self.driver.current_url
        try:
            result_targets = self.driver.find_elements_by_xpath("//div[@id='variation_color_name']/ul/li")
            for target_tmp in result_targets:
                img_target = target_tmp.find_element_by_tag_name("img")
                result_temp = img_target.get_attribute("alt")
                if select_id == result_temp:
                    self.driver.execute_script("arguments[0].click();", target_tmp.find_element_by_tag_name("button"))
        except Exception, e:
            self.openUrl(current_url, "add-to-cart-button")

    def select_size_target(self, select_id=None):
        self.waitForReloadFinish("add-to-cart-button")
        if select_id is None or select_id == "":
            return
        current_url = self.driver.current_url
        try:
            actions = ActionChains(self.driver)
            searchDropDown = self.driver.find_element_by_id('native_dropdown_selected_size_name')
            actions.move_to_element(searchDropDown)
            actions.click_and_hold(searchDropDown)
            actions.perform()
            waitRandomSecons()
            select = Select(searchDropDown)
            select.select_by_visible_text(select_id)
            actions.send_keys(Keys.RETURN).perform()
        except Exception, e:
            self.openUrl(current_url, "add-to-cart-button")

    def browse_product_page(self, checkId="add-to-cart-button"):
        """add item to cart"""
        current_url = self.driver.current_url
        self.waitForReloadFinish(checkId)
        self.scroll_to_target("title", scroll_time=1)
        waitRandomSecons()
        try:
            self.check_some_alt_images()
            browser_type = random.randint(0, 2)
            if browser_type == 0:
                self.see_other_product()
            if browser_type == 1:
                self.view_qa()
            self.scroll_to_target("dp-customer-review-header", False, 5, 'ask_lazy_load_div')
            if browser_type == 2:
                self.view_bad_view()
        except Exception, e:
            self.openUrl(current_url)

        self.scroll_to_target("reviews-medley-footer", True, 20, "dp-customer-review-header")
        self.scroll_to_target("altImages", True, 3, "reviews-medley-footer")

    def add_to_cart(self, child_asin_id=None, checkId="add-to-cart-button"):
        """add item to cart"""
        self.waitForReloadFinish(checkId)
        if child_asin_id is not None:
            try:
                target = self.driver.find_element_by_xpath("//li[@data-defaultasin='%s']" % child_asin_id)
                target = target.find_element_by_tag_name("button")
                target.click()
                self.waitForReloadFinish(checkId)
            except Exception, e:
                pass
        current_url = self.driver.current_url
        print '================start to add item to cart==================='
        add_to_car = True
        try:
            add_to_shopping_cart_target = self.driver.find_element_by_id("a-autoid-0-announce")
            #self.driver.execute_script("arguments[0].click();", add_to_shopping_cart_target)
            add_to_shopping_cart_target.click()
            add_to_car = False
        except Exception, e:
            pass
        waitRandomSecons(5)
        if add_to_car:
            add_to_shopping_cart_target = self.driver.find_element_by_id(checkId)
            self.driver.execute_script("arguments[0].click();", add_to_shopping_cart_target)
            self.waitForAddingShoppingCardFinish()
        print '================successfully add to cart==================='
        self.openUrl(current_url, checkId)

    def add_to_wish(self, child_asin_id=None, checkId="add-to-wishlist-button-submit"):
        # add to wish list
        self.waitForReloadFinish(checkId)
        if child_asin_id is not None:
            try:
                target = self.driver.find_element_by_xpath("//li[@data-defaultasin='%s']" % child_asin_id)
                target = target.find_element_by_tag_name("button")
                log_info("found child asin by id: " + child_asin_id)
                target.click()
                self.waitForReloadFinish(checkId)
            except Exception, e:
                pass
        self.scroll_to_target(checkId, scroll_time=3, ignore_final=False)
        current_url = self.driver.current_url
        print '================start to add item to wish list==================='
        self.driver.find_element_by_id(checkId).click()
        self.waitForAddingWishFinish("WLHUC_continue", "wishlist-page")
        waitRandomSecons()
        self.openUrl(current_url, checkId)
        print '================successfully add to wish list==================='

    def exit_driver(self):
        """exit the webdriver"""
        try:
            self.driver.quit()
        except Exception, e:
            print 'Error while exiting the web driver\n%s' % e.message

    def sign_up(self, sign_up_form):
        """sign up with randomly generate user

        Args:
            sign_up_form (dict): some infomation required to sign up: name, e-mail and password
            sign_up_url (str, optional): url to sign up, custom url can jumps to the target url after signing up
        """
        self.openUrl(self.amazon_index, "nav-link-accountList")
        self.driver.find_element_by_id("nav-link-accountList").click()
        self.waitForReloadFinish("createAccountSubmit")
        createAccount = self.driver.find_element_by_id("createAccountSubmit")
        createAccount.click()
        self.waitForReloadFinish("ap_customer_name")
        inputElement = None
        try:
            for k, v in sign_up_form.items():
                inputElement = self.driver.find_element_by_name(k)
                inputElement.send_keys(v)
            inputElement.submit()
            user_info = User(sign_up_form['email'], sign_up_form['password'])
            self.waitForReloadFinish("nav-link-accountList")
            return user_info
        except Exception, e:
            # self.save_identify_code()
            print 'Error while signing up\n%s' % e.message
            return None

    def writeToNewUserFile(*data):
        with open("../data/ipUserData.txt", 'a') as f:
            f.write(str(data) + "\n")
        f.close()


if __name__ == '__main__':
    robot = RobotBrowser()
    robot.imagesget(
        "https://opfcaptcha-prod.s3.amazonaws.com/1bbce51192c84819b717b35c3929c19a.jpg?AWSAccessKeyId=AKIAIQ42SCAGCLB5JKMA&Expires=1502380672&Signature=D6N86elW1TUBqH7PBihBou9uXXI%3D")





