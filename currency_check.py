from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time

currency_dict = {'GBP':'英镑',
'HKD':'港币',
'USD':'美元',
'CHF':'瑞士法郎',
'DEM':'德国马克',
'FRF':'法国法郎',
'SGD':'新加坡元',
'SEK':'瑞典克朗',
'DKK':'丹麦克朗',
'NOK':'挪威克朗',
'JPY':'日元',
'CAD':'加拿大元',
'AUD':'澳大利亚元',
'EUR':'欧元',
'MOP':'澳门元',
'PHP':'菲律宾比索',
'THP':'泰国铢',
'NZD':'新西兰元',
'KPW':'韩元',
'SUR':'卢布',
'MYR':'林吉特',
'TWD':'新台币',
'ESP':'西班牙比塞塔',
'ITL':'意大利里拉',
'NLG':'荷兰盾',
'BEF':'比利时法郎',
'FIM':'芬兰马克',
'INR':'印度卢比',
'IDR':'印尼卢比',
'BRC':'巴西里亚尔',
'AED':'阿联酋迪拉姆',
'ZAR':'南非兰特',
'SAR':'沙特里亚尔',
'TRL':'土耳其里拉'}


def format_date(date_str):
    # 将日期从"YYMMDD"格式转换成"YYYY-MM-DD"格式
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"


def get_forex_rate(date, currency_code):
    driver = webdriver.Chrome()
    try:
        driver.get('https://www.boc.cn/sourcedb/whpj/')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'pjname')))

        # 转换日期格式
        formatted_date = format_date(date)

        # 等待日期输入框加载
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'erectDate')))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'nothing')))

        currency_select = Select(driver.find_element(By.ID, 'pjname'))
        currency_select.select_by_visible_text(currency_dict[currency_code])

        # 填入起始日期和结束日期
        start_date_input = driver.find_element(By.ID, 'erectDate')
        end_date_input = driver.find_element(By.ID, 'nothing')

        start_date_input.clear()
        end_date_input.clear()

        start_date_input.send_keys(formatted_date)
        end_date_input.send_keys(formatted_date)

        button = driver.find_element(By.XPATH, '//input[@onclick="executeSearch()"]')
        button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.wrapper > div.BOC_main.publish')))
        time.sleep(2)  # 稍等2秒确保数据加载完成

        # 定位元素
        #
        rate = driver.find_element(By.CSS_SELECTOR, 'body > div.wrapper > div.BOC_main.publish > table > tbody > tr:nth-child(2) > td:nth-child(4)')
        with open('result.txt', 'w') as f:
            f.write(rate.text.strip())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 yourcode.py <date> <currency_code>")
    else:
        date = sys.argv[1]
        currency_code = sys.argv[2]
        get_forex_rate(date, currency_code)
