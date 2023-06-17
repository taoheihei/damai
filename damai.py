import os
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import pandas as pd
import requests
import json

class DaMaiTicket:
  def __init__(self) -> None:
    self.loginId = 'taoheihei'
    self.loginPwd = 'xxxxxxxx'
    self.itemId = '723684422858' #对应的要抢票的id
    self.classDate = '2023-06-23' #具体到天
    self.priceStr = '388'
    self.ticketCount = 1
    self.viewers = ["鸣人", "佐助"]
    self.grabMinute = 0 # 抢票的分钟
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("disable-blink-features=AutomationControlled")
    # chrome_option.add_argument("--user-data-dir={}".format(USER_DIR))
    self.browser =webdriver.Chrome( chrome_options=chrome_option)
    with open("stealth.min.js", "r", encoding="utf-8") as f:
      js_code = f.read()
  #防止selenium被认出来,隐藏其特征
    self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
      "source": js_code
    })
    self.browser.maximize_window()

  def find_element(self, xpath):
    try:
      element = WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
      return element
    except Exception as e:
      print(e)
      return None


  def start(self):
    self.login()
    time.sleep(1)
    self.browser.get('https://m.damai.cn/damai/detail/item.html?itemId='+ self.itemId)
    # while True:
    #   if time.localtime().tm_min == self.grabMinute:
    #     self.choose()
    self.choose()
  #选票（立即购买）
  def choose(self):

    self.find_element('//div[@class="buy__button"]').click()
    self.find_element('//div[@class="bui-dm-sku-card-item-box" and contains(., "'+ self.classDate +'")]//div[@class="item-content"]').click()
    self.find_element('//div[contains(@class, "sku-tickets-card")]//div[contains(@class,"item-content") and  contains(.,"'+ self.priceStr +'")]')
    if self.ticketCount > 1:
      defalutTicket = 1
      while(defalutTicket<self.ticketCount):
        self.find_element('//div[@class="number-edit"]//div[@class="number-edit-bg"][2]')
        defalutTicket= defalutTicket + 1
    self.find_element('//div[@class="sku-footer-bottom"]//div[contains(@class, "sku-footer-buy-button")]').click()
    for viewer in self.viewers:
      self.find_element('//div[@class="viewer"]/div/div[contains(.,"'+ viewer +'")]//i')
    self.find_element('//div[contains(@data-spm, "dmSubmit")]//div[@view-name="TextView" and .="提交订单"]/span').click()


  #登录
  def login(self):
    self.browser.get('https://m.damai.cn/damai/minilogin/index.html')
    self.find_element('//div[contains(@class, "login-links")]/a').click()
    self.find_element('//input[@id="fm-login-id"]').send_keys(self.loginId)
    self.find_element('//input[@id="fm-login-password"]').send_keys(self.loginPwd)
    self.find_element('//div[@class="fm-btn"]/button').click()

  def close(self):
    self.browser.close()

if __name__ == '__main__':
  damai = DaMaiTicket()
  damai.start()
  damai.close()