# -*- coding: utf-8 -*-
# @Author: LC
# @Date:   2016-07-04 21:04:49
# @Last modified by:   LC
# @Last Modified time: 2016-08-14 10:57:52
# @Email: liangchaowu5@gmail.com

##########################################################################
# Function: 
# 1. fetch proxies from site: http://www.xicidaili.com/,store them in redis
# 2. get a valid proxy for a certain site 
##########################################################################




from manager.DataManager import *


import json


dataPath = os.path.abspath("./data")
proxyDataPath = os.path.join(dataPath, "proxyIp.txt")





def writeToFile(data):
    with open(proxyDataPath, 'a') as f:
        f.write(data+"\n")
    f.close()

def get_proxies(proxy_type, ip_set, start_page, end_page):
    """extract proxies from page source code, store them in redis
    
    Args:
        proxy_type (str): base url for proxy type, like the global variables CHINA and OTHER
        ip_set (str): which set should the ips be stored in redis
        start_page (int):  which page to start crawling
        end_page (int): which page to stop crawling

    try:
        conn = get_connection()
    except Exception:
        print 'Error while connecting to redis'
        return
            """
    allData = DataManager()
    proxies, curr_proxy =[], None
    for page in xrange(start_page, end_page+1):
        if page % 2 == 0:
            time.sleep(20)
        # get page source code
        headers = {'user-agent': generate_user_agent(), 'referer': 'http://www.xicidaili.com/'}
        text = requests.get(proxy_type+str(page), headers = headers).text
        # extract ips from source code
        soup = BeautifulSoup(text, 'lxml')
        for tr in soup.find_all('tr')[1:]:
            tds = tr.find_all('td')
            #if u'美国' in tds[3].text:
            proxy = tds[1].text+':'+tds[2].text               
            if is_valid(proxy):
                if proxy not in proxies:
                    print proxy
                    sign_up_success = True
                    while sign_up_success:
                        robot = RobotBrowser()
                        ran_index = random.randint(0, len(allData.userNames))
                        sign_up_form = robot.generate_sign_up_user(allData.userNames[ran_index], True)

                        userInfo = robot.sign_up(sign_up_form)
                        if userInfo != None:
                            allData.writeToFile(allData.userDataPath, userInfo)
                            proxies.append(proxy)
                            writeToFile(proxy)
                        else:
                            sign_up_success = False


def get_proxy_ip_from_database(table_name="amazon"):
      proxyUrls=[]
      ids = sql_driver.get_proxy_ids(table_name)
      for id in ids:
          proxy_tmp = sql_driver.get_proxy_with_id(table_name=table_name,id=id)
          proxyUrls.append(proxy_tmp.ip+":"+str(proxy_tmp.port))
      log_info("update proxy ip: "+str(len(proxyUrls)))
      return proxyUrls

def get_proxy_ip(requestUrl):
      proxyUrls=[]

      req=urllib2.Request(requestUrl)
      res=urllib2.urlopen(req)
      while True:
           line=res.readline()
           if line:
                if line!='\n':
                     line=line.strip()
                     writeToFile(line)
                     proxyUrls.append(line)
                else:
                     pass
           else:
                break
      log_info("update proxy ip："+str(len(proxyUrls)))
      return proxyUrls


def is_valid(ip, target_url=AMAZON_PATH, referer=AMAZON_PATH):
    """judge if a proxy ip is valid for target_url

    Args:
        target_url (str): url that need to visite with a proxy
        ip (str): the set in redis to get 
        referer (str, optional): referer part of  headers  of the request
    
    Returns:
        boolean
    """
    proxy = {
    'http': 'http://%s' %ip
    }
    headers = {'user-agent': generate_user_agent(), 'referer': referer}
    try:
        r = requests.get(target_url, headers = headers, proxies = proxy, timeout = 6)
        return True
    except Exception:
        return False

def is_chinese_ip(ip,target_url="http://freegeoip.net/json/"):
    result = get_proxy_content(target_url,ip)
    if result == None:
        return False
    try:
        data = json.loads(result)
        coutry = data.get("country_name")
        log_info(ip +"is located in " +coutry)
        if data.get("country_name") == "China":
            return True
        return False
    except Exception,e:
        return False

def get_proxy_content(target_url, ip):
    """judge if a proxy ip is valid for target_url

    Args:
        target_url (str): url that need to visite with a proxy
        ip (str): the set in redis to get
        referer (str, optional): referer part of  headers  of the request

    Returns:
        boolean
    """
    proxy = {
        'http': 'http://%s' % ip
    }
    headers = {'user-agent': generate_user_agent()}
    try:
        r = requests.get(target_url, headers=headers, proxies=proxy, timeout=30)
        return r.content
    except Exception:
        return None


def update_proxy_location(table_name="amazon"):
    target_url = r"http://freegeoip.net/json/"
    count = 0
    ids = sql_driver.get_proxy_ids(table_name)
    for id in ids:
        proxy_tmp = sql_driver.get_proxy_with_id(table_name=table_name, id=id)
        result = get_proxy_content(target_url,proxy_tmp.ip+":"+str(proxy_tmp.port))
        time.sleep(3)
        print result
        if result is not None:
            try:
                data = json.loads(result)
                country_name = data.get("country_name")
                if country_name is not None and proxy_tmp.country != country_name:
                    proxy_tmp.country = country_name
                    sql_driver.update_proxy(table_name=table_name, proxy=proxy_tmp)
                    sql_driver.commit()
                    count = count + 1
                    log_info("update " + proxy_tmp.ip)
            except Exception,e:
                continue

    log_info("update proxy ip：" + str(count))

if __name__ == '__main__':
    update_proxy_location()
    update_proxy_location(table_name="http_bin")
    update_proxy_location(table_name="free_ipproxy")