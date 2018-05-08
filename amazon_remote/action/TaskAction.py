# -*- coding: utf-8 -*-

from manager.DataManager import *
from manager.RegistUser import *
from commonException.AuthException import *
from RobotBrowser import *
import threading
import sys
import random

class TaskAction:
    def __init__(self, task_temp):

        self.data_manager = DataManager()
        self.task_data = task_temp
        self.all_user_names = self.data_manager.userNames
        self.all_ip_users = self.data_manager.allIPUser
        self.all_look_and_look_urls = self.data_manager.look_and_look_urls
        self.all_proxy_ip = self.data_manager.allProxyIp

        self.all_used_proxy = []

        self.all_run_time = 0
        self.lock = threading.Lock()

    def run_one_time(self, email, proxy_ip=None):
        self.lock.acquire()
        try:
            self.all_run_time = self.all_run_time + 1
            log_info("------------run " + email + " success-----------total count: " + str(self.all_run_time))
            if self.all_run_time > int(self.task_data.run_count):
                log_info("-------------run finish, total count is " + str(self.all_run_time))
                return True
            return False
        except Exception, e:
            pass
        finally:
            self.lock.release()

    def get_one_proxy(self):

        self.lock.acquire()
        try:
            if len(self.all_proxy_ip) == 0:
                log_info("proxy ip runs out.")
                return None
            return self.all_proxy_ip.pop(random.randint(0, len(self.all_proxy_ip)-1))
        except Exception, e:
            pass
        finally:
            self.lock.release()

    def update_ip_user(self, proxy_ip, user_data):
        self.lock.acquire()
        try:
            self.all_ip_users[proxy_ip] = user_data
            self.data_manager.updataIpUser(self.all_ip_users)
        except Exception, e:
            log_error("update ip users failed.")
            sys.exit(0)
        finally:
            self.lock.release()
        return None

    def get_one_user(self, key):
        if key is None:
            return None
        key = str(key).strip("\n")
        self.lock.acquire()
        try:
            if len(self.all_ip_users) == 0:
                log_info("user accounts runs out.")
                sys.exit(0)
            return self.all_ip_users[key]
        except Exception, e:
            log_error(e.message)
        finally:
            self.lock.release()
        return None



    def task_thread_for_wish_car(self):
        proxy_ip = None
        use_new_browser = True
        while True:
            if isTimeToEnd(self.task_data.end_time):
                break
            if use_new_browser:
                proxy_ip = self.get_one_proxy()
                if proxy_ip is None:
                    break
            user = self.get_one_user(proxy_ip)
            robot_work = RobotBrowser(proxy_ip)
            try:
                if user is None or user == "":
                    user_info = generate_sign_up_user(
                        self.all_user_names[random.randint(0, len(self.all_user_names) - 1)], True)
                    result = robot_work.sign_up(user_info)
                    if result is not None:
                        user = User(user_info['email'], user_info['password'])
                        self.update_ip_user(proxy_ip, user)

                else:
                    robot_work.sign_in(user)
                log_info("current running user is " + user.email)
                robot_work.search_keywords(self.task_data.key_word, self.task_data.asin_id, self.task_data.max_page,
                                           self.task_data.search_type)
                robot_work.browse_product_page()
                if self.task_data.like_5_point_comment == "yes":
                    robot_work.comment_like()
                if self.task_data.select_child_product == "yes" and self.task_data.child_asin_id is not None:
                    for child_asn_id_tmp in self.task_data.child_asin_id:
                        if self.task_data.add_to_wish == "yes":
                            robot_work.add_to_wish(child_asin_id=child_asn_id_tmp)
                        if self.task_data.add_to_cart == "yes":
                            robot_work.add_to_cart(child_asin_id=child_asn_id_tmp)
                else:
                    if self.task_data.add_to_wish == "yes":
                        robot_work.select_color_target(self.task_data.color)
                        robot_work.select_size_target(self.task_data.size)
                        robot_work.add_to_wish()
                    if self.task_data.add_to_cart == "yes":
                        robot_work.select_color_target(self.task_data.color)
                        robot_work.select_size_target(self.task_data.size)
                        robot_work.add_to_cart()
                log_info("run task using user : " + user.email + " finish.")
                robot_work.exit_driver()
                if self.run_one_time(user.email, proxy_ip):
                    break
                use_new_browser = True
            except LoginException, e:
                log_error(e.message)
                self.update_ip_user(proxy_ip, None)
                log_error("delete user " + user.email)
                use_new_browser = False
            except AuthException, e:
                log_error(e.message)
                robot_work.exit_driver()
                use_new_browser = True
            except Exception, e:
                log_error(e.message)
                robot_work.exit_driver()
                use_new_browser = True
            finally:
                waitRandomSecons()

    def task_thread_for_look_and_look(self):
        while True:
            proxy_ip = self.get_one_proxy()
            robot = RobotBrowser(proxy_ip)
            all_count = len(self.all_look_and_look_urls)
            count = 0
            for url in self.all_look_and_look_urls:
                count = count + 1
                if count == all_count:
                    robot.openUrl(url)
                else:
                    robot.driver.execute_script("window.open(arguments[0]);", url)
            log_info("open " + str(count) + " pages.")
            waitSeconds(30)
            robot.exit_driver()
            self.run_one_time("look_and_look", proxy_ip)

    def check_thread(self,type="Small"):
        robot_work = RobotBrowser()
        robot_work.openUrl("https://www.amazon.com/Waterproof-Camouflage-Military-Tactical-camouflage/dp/B0743CL7H6/ref=sr_1_18?ie=UTF8&qid=1503051334&sr=8-18&keywords=hunting%2BJacket&th=1&psc=1")
        # actions = ActionChains(robot_work.driver)
        # search_drop_down = robot_work.driver.find_element_by_name('dropdown_selected_size_name')
        # actions.move_to_element(search_drop_down)
        # actions.click_and_hold(search_drop_down)
        # actions.perform()
        # waitRandomSecons()
        # select = Select(search_drop_down)
        # select.select_by_visible_text(type)
        # click_target=robot_work.driver.find_element_by_name("dropdown_selected_size_name")B01M7PEGLQ B01M7P9WUG
        result_targets = robot_work.driver.find_elements_by_xpath("//div[@id='variation_color_name']/ul/li")
        for target_tmp in result_targets:
            img_target = target_tmp.find_element_by_tag_name("img")
            result_temp = img_target.get_attribute("alt")
            if 'Jacket and Pants' == result_temp:
                robot_work.driver.execute_script("arguments[0].click();", target_tmp.find_element_by_tag_name("button"))
        robot_work.waitForReloadFinish("add-to-cart-button")
        try:
            result_targets = robot_work.driver.find_elements_by_xpath("//select[@name='dropdown_selected_size_name']/option")
        except Exception,e:
            result_targets = robot_work.driver.find_elements_by_xpath("//select[@name='dropdown_selected_size_name']/option")

        actions = ActionChains(robot_work.driver)
        searchDropDown = robot_work.driver.find_element_by_id('native_dropdown_selected_size_name')
        actions.move_to_element(searchDropDown)
        actions.click_and_hold(searchDropDown)
        actions.perform()
        waitRandomSecons()
        select = Select(searchDropDown)
        select.select_by_visible_text(type)
        actions.send_keys(Keys.RETURN).perform()

        # is_final = False
        # for target_tmp in result_targets:B01M7P9WUG
        #     text_temp = str(target_tmp.text)
        #     if type == text_temp:
        #         robot_work.driver.execute_script("arguments[0].selected=true;", target_tmp)
        #         robot_work.driver.execute_script("var event = document.createEvent('HTMLEvents');event.initEvent('change',true,false);arguments[0].dispatchEvent(event);",target_tmp)
        #         is_final = True
        #     elif type in str(target_tmp.text) and not is_final:
        #         robot_work.driver.execute_script("arguments[0].selected=true;", target_tmp)
        #         robot_work.driver.execute_script("var event = document.createEvent('HTMLEvents');event.initEvent('change',true,false);arguments[0].dispatchEvent(event);",target_tmp)
        waitSeconds(1000)

    def start_action_work(self):
        log_info("############################## start to run one task. ################################")
        isTimeToGo(self.task_data.start_time)
        thread_count = int(self.task_data.task_count)
        task_type = self.task_data.task_type
        if task_type == "shopping_cart_wish":
            task = self.task_thread_for_wish_car
        elif task_type == "look_and_look":
            task = self.task_thread_for_look_and_look
        else:
            log_error("task type " + task_type + " is wrong.")
            sys.exit(0)
        all_thread_tasks = []
        for i in range(thread_count):
            t1 = threading.Thread(target=task, args=())
            all_thread_tasks.append(t1)
            t1.start()
        for task in all_thread_tasks:
            task.join()
        log_info("############################## run one task finish. ##################################")







