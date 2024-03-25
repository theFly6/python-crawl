import sys
import os
import json
from datetime import datetime
from spiderTools import ForeignExchangeQuerySpider, StandardCurrencySpider


class QueryManager:
    """ 外汇查询控制器类，用于获取指定货币某个日期的“现汇卖出价”，
        然后调度spiderTools中的爬虫进行selenium数据爬取、清洗、保存操作

    Attributes:
        currency_time(str): 用户输入的货币日期
        currency_code(str): 用户输入的货币代号
        data(List[dict]): 标准货币符号数据集
        currency_ftime(dict): 格式化后的货币日期
        currency_fcode(str): 格式化后的货币名称
    """
    def __init__(self, currency_time: str, currency_code: str) -> None:
        """初始化并格式化货币日期、代号，准备标准货币符号数据集"""
        self.currency_time = currency_time
        self.currency_code = currency_code

        # 加载标准货币符号数据集
        self.data = self.load_data('Code2Chinese.json')

        # 检查参数的合法性并格式化两个参数
        self.currency_ftime = None
        self.currency_fcode = None
        self.standard_input()

    def manage(self):
        """爬虫控制主调函数"""
        query_time = self.currency_ftime
        query_currency = self.currency_fcode['货币名称 中文']
        feqspider = ForeignExchangeQuerySpider()
        feqspider.parse(query_time, query_currency)
        print('——'*30)
        print(f'输入:{query_time}, {self.currency_code}({query_currency})')
        feqspider.print_example()
        feqspider.save(f'result_{self.currency_time}_{self.currency_code}.txt')
        print('——'*30)
        


    def load_data(self, file_name: str):
        """标准货币符号数据集加载函数"""
        if not os.path.exists(file_name):
            print(f'没有检测到"{file_name}"文件，正在爬取数据到{file_name}，请稍等……')
            scspider = StandardCurrencySpider()
            scspider.gen_trans_json(file_name)
        with open(file_name, 'r', encoding='utf8') as file:
            return json.load(file)

    def standard_input(self):
        """监测并格式化处理用户输入"""
        try:
            self.currency_fcode = [country_info for country_info in self.data if country_info['标准符号']==self.currency_code]
            self.currency_fcode = self.currency_fcode[0]
        except:
            raise Exception('你输入的货币代号有误，请重新输入！')
        
        try:
            self.currency_ftime = datetime.strptime(self.currency_time, '%Y%m%d')
            self.currency_ftime = str(self.currency_ftime).split(' ')[0]
        except ValueError:
            raise Exception("你输入的日期不合法，请重新输入！")


if __name__ == '__main__':
    # 获取命令行参数
    param_time = sys.argv[1]
    param_code = sys.argv[2]
    # 创建爬虫调度器
    qm = QueryManager(param_time, param_code)
    # 运行爬虫主调函数
    qm.manage()

    # 一般情况
    # python manager.py 20221023 SUR
    # python manager.py 20211231 USD
    # 结果正常

    # 日期在未来的情况（没有数据）
    # python manager.py 20251231 USD
    # 所有此类结果报错：Exception: 这天的数据好像走丢啦！
    # 结果正常

    # 错误情况
    # python manager.py 20211231 JPY
    # JPY在标准符号对照网站上对应的是“日圆”
    # 但是中国银行的牌价上为“日元”
    # 所有此类参照不同的情况均会报错：Exception: 真是不好意思，好像没有与您指定的货币代号对应的选项呢！
    # 结果正常
