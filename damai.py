
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class DaMaiTicket:
  def __init__(self) -> None:
    self.loginId = 'account'
    self.loginPwd = 'password'
    self.itemId = '717541618637' #对应的要抢票的id
    self.classDate = '2023-07-16' #具体到天，如果演唱会只有1天，可以不选
    self.priceStr = '180' #票价
    self.ticketCount = 2
    self.viewers = ["鸣人", "佐助"]
    self.grabMinute = 0 # 抢票的时间分钟，在快要抢票的时候打开
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument("disable-blink-features=AutomationControlled")
    # chrome_option.add_argument("--user-data-dir={}".format(USER_DIR))
    self.browser =webdriver.Chrome(options=chrome_option)
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
      self.browser.execute_script("arguments[0].scrollIntoView();", element)
      time.sleep(0.5)
      return element
    except Exception as e:
      print(e)
      return None

  def get_elementLen(self, xpath):
    try:
      WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, xpath)))
      time.sleep(0.5)
      eleLen = len(self.browser.find_elements(xpath))
      return eleLen
    except Exception as e:
      print(e)
      return 0

  def start(self):
    self.login()
    time.sleep(1)
    self.browser.get('https://m.damai.cn/damai/detail/item.html?itemId='+ self.itemId)
    while True:
      if time.localtime().tm_min == self.grabMinute:
        self.choose()
    # self.choose()
  #选票（立即购买）
  def choose(self):

    self.find_element('//div[@class="buy__button"]').click()
    #如果场次大于等于2场要选场次
    if self.get_elementLen('//div[contains(@class, "sku-times-card")]//div[contains(@class,"item-content")]') > 1:
        self.find_element('//div[@class="bui-dm-sku-card-item-box" and contains(., "'+ self.classDate +'")]//div[@class="item-content"]').click()
    self.find_element('//div[contains(@class, "sku-tickets-card")]//div[contains(@class,"item-content") and  contains(.,"'+ self.priceStr +'")]').click()
    if self.ticketCount > 1:
      defalutTicket = 1
      while(defalutTicket<self.ticketCount):
        self.find_element('//div[@class="number-edit"]//div[@class="number-edit-bg"][2]').click()
        defalutTicket= defalutTicket + 1
    self.find_element('//div[@class="sku-footer-bottom"]//div[contains(@class, "sku-footer-buy-button")]').click()
    for viewer in self.viewers:
      self.find_element('//div[@class="viewer"]/div/div[contains(.,"'+ viewer +'")]//i').click()
    self.find_element('//div[contains(@data-spm, "dmSubmit")]//div[@view-name="TextView" and .="提交订单"]/span').click()


  #登录
  def login(self):
    self.browser.get('https://m.damai.cn/damai/minilogin/index.html')
    WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//iframe[@id="alibaba-login-box"]')))
    self.browser.switch_to.frame('alibaba-login-box')
    self.find_element('//div[contains(@class, "login-links")]/a').click()
    self.find_element('//input[@id="fm-login-id"]').send_keys(self.loginId)
    self.find_element('//input[@id="fm-login-password"]').send_keys(self.loginPwd)
    self.find_element('//div[@class="fm-btn"]/button').click()
    self.browser.switch_to.default_content()
    time.sleep(2)

  def close(self):
    self.browser.close()

if __name__ == '__main__':
  damai = DaMaiTicket()
  damai.start()
  # damai.close()