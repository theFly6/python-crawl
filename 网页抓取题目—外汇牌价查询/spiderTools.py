from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement

import json
import time

class StandardCurrencySpider:
    """标准货币符号数据集爬取爬虫"""
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.country_infos = []
    
    def gen_trans_json(self, file_name='Code2Chinese.json'):
        """提取标准货币符号数据并保存为指定名称的文件"""
        self.driver.get('https://www.11meigui.com/tools/currency')
        tr_elements = self.driver.find_elements(By.XPATH, '//table/tbody/tr[position() >= 3]')

        for tr_element in tr_elements:
            td_elements = tr_element.find_elements(By.XPATH, './td')
            td_texts=[td.text.strip() for td in td_elements]
            if(len(td_texts)==6):
                country_info = {
                    '国别': td_texts[0],
                    '货币名称 中文':  td_texts[1],
                    '货币名称 英文':  td_texts[2],
                    '原有旧符号': td_texts[3],
                    '标准符号': td_texts[4],
                    '辅币进位制': td_texts[5],
                }
                self.country_infos.append(country_info)
        
        # 保存获取的标准国家货币符号数据到json文件中
        with open(file_name, 'w', encoding='utf8')as f:
            print(f'货币代号转换表"{file_name}"文件生成成功')
            f.write(json.dumps(self.country_infos, ensure_ascii=False, indent=4))
        self.driver.close()


class ForeignExchangeQuerySpider:
    """指定日期及货币符号货币信息查询爬虫
    
    """
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.foreign_exchange_infos = []
    
    def parse(self, query_time, query_currency):
        """根据传入的查询日期与货币名称解析目标货币查询网站"""
        self.driver.get('https://www.boc.cn/sourcedb/whpj/')
        self.fill_form(query_time, query_time, query_currency).click()
        self.collect_res()
        self.driver.close()
    
    def print_example(self):
        """打印一个示例输出（默认筛选后爬取页面的第一行数据并保持到result.txt文件中）"""
        with open('result.txt', 'w', encoding='utf8')as f:
            f.write(self.foreign_exchange_infos[0]['现汇卖出价'])
        print('输出：', self.foreign_exchange_infos[0]['现汇卖出价'], '(结果在"result.txt"文件中)')
    
    def save(self, file_name='result.json'):
        """保存self.foreign_exchange_infos列表中获取到的所有结果数据到指定文件"""
        with open(file_name, 'w', encoding='utf8')as f:
            f.write(json.dumps(self.foreign_exchange_infos, ensure_ascii=False, indent=4))
            print(f'(查询成功，完整结果保存在"{file_name}"文件)')

    def fill_form(self, start_time, end_time, currency)->WebElement:
        """Selenium自动化填表单并返回提交按钮元素对象"""
        start_time_element = self.driver.find_element(By.XPATH,'//*[@id="erectDate"]')
        self.driver.execute_script(f"arguments[0].setAttribute('value', '{start_time}')", start_time_element)
        
        end_time_element = self.driver.find_element(By.XPATH,'//*[@id="nothing"]')
        self.driver.execute_script(f"arguments[0].setAttribute('value', '{end_time}')", end_time_element)
        
        currency_element = self.driver.find_element(By.XPATH,'//*[@id="pjname"]')
        currency_select = Select(currency_element)
        try:
            currency_select.select_by_visible_text(currency)
        except Exception as e:
            raise Exception('真是不好意思，好像没有与您指定的货币代号对应的选项呢！')
        return self.driver.find_element(By.XPATH,'//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input')

    def collect_res(self):
        """将结果页面的所有数据收集到一个名为self.foreign_exchange_infos的列表中"""
        time.sleep(0.5)
        err_msg = '对不起，没有检索结果，请换其他检索词重试！'
        if err_msg in self.driver.page_source:
            raise Exception('这天的数据好像走丢啦！')
        tr_elements = self.driver.find_elements(By.XPATH, '//table/tbody/tr[position() >= 3]')
        for tr_element in tr_elements:
            td_elements = tr_element.find_elements(By.XPATH, './td')
            td_texts=[td.text.strip() for td in td_elements]
            if(len(td_texts)==7):
                foreign_exchange_info = {
                    "货币名称": td_texts[0],
                    "现汇买入价": td_texts[1],
                    "现钞买入价": td_texts[2],
                    "现汇卖出价": td_texts[3],
                    "现钞卖出价": td_texts[4],
                    "中行折算价": td_texts[5],
                    "发布时间": td_texts[6]
                }
                self.foreign_exchange_infos.append(foreign_exchange_info)