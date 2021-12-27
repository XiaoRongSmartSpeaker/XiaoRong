#coding='utf-8'
from selenium import webdriver

class WorldTime:

    def find_time_from_web():
        url = 'http://tool.ckd.cc/worldclock.php'
        browser = webdriver.Firefox()  # 启动浏览器
        browser.get(url)   # 打开网页
        elements = browser.find_elements_by_css_selector('body > table:nth-child(4) > tbody')  
        #print(type(elements))
        for element in elements:
            print(element.text)
        # 关闭并退出浏览器
        browser.close()
        browser.quit()
        
