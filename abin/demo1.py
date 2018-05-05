from __future__ import print_function
from __future__ import division

import warnings

from abupy.TLineBu.ABuTLine import AbuTLine

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
import abupy
from abupy import AbuFactorBuyXD, BuyCallMixin
from abupy import ABuPickTimeExecute
from abupy import AbuFactorAtrNStop
from abupy import AbuFactorPreAtrNStop
from abupy import AbuFactorCloseAtrNStop
from abupy import AbuFactorSellXD, ESupportDirection
from abupy.BetaBu import AbuABinPosition
# run_loop_back等一些常用且最外层的方法定义在abu中
from abupy import abu, ABuProgress# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
from abupy import AbuMetricsBase

#是否使用测试
#abupy.env.enable_example_env_ipython()

class AbuFactorBuyBreak(AbuFactorBuyXD, BuyCallMixin):
    """示例继承AbuFactorBuyXD完成正向突破买入择时类, 混入BuyCallMixin，即向上突破触发买入event"""
    def fit_day(self, today):
        """
        针对每一个交易日拟合买入交易策略，寻找向上突破买入机会
        :param today: 当前驱动的交易日金融时间序列数据
        :return:
        """
        # 今天的收盘价格达到xd天内最高价格则符合买入条件
        if today.close == self.xd_kl.close.max():
            # 生成买入订单, 由于使用了今天的收盘价格做为策略信号判断，所以信号发出后，只能明天买
            return self.buy_tomorrow()
        return None

class AbuSDBreak(AbuFactorBuyXD, BuyCallMixin):
    """示例买入因子： 在AbuFactorBuyBreak基础上进行降低交易频率，提高系统的稳定性处理"""

    def _init_self(self, **kwargs):
        """
        :param kwargs: kwargs可选参数poly值，poly在fit_month中和每一个月大盘计算的poly比较，
        若是大盘的poly大于poly认为走势震荡，poly默认为2
        """
        super(AbuSDBreak, self)._init_self(**kwargs)
        # poly阀值，self.poly在fit_month中和每一个月大盘计算的poly比较，若是大盘的poly大于poly认为走势震荡
        self.poly = kwargs.pop('poly', 2)
        # 是否封锁买入策略进行择时交易
        self.lock = False

    def fit_month(self, today):
        # fit_month即在回测策略中每一个月执行一次的方法
        # 策略中拥有self.benchmark，即交易基准对象，AbuBenchmark实例对象，benchmark.kl_pd即对应的市场大盘走势
        benchmark_df = self.benchmark.kl_pd
        # 拿出大盘的今天
        benchmark_today = benchmark_df[benchmark_df.date == today.date]
        if benchmark_today.empty:
            return 0
        # 要拿大盘最近一个月的走势，准备切片的start，end
        end_key = int(benchmark_today.iloc[0].key)
        start_key = end_key - 20
        if start_key < 0:
            return False

        # 使用切片切出从今天开始向前20天的数据
        benchmark_month = benchmark_df[start_key:end_key + 1]
        # 通过大盘最近一个月的收盘价格做为参数构造AbuTLine对象
        benchmark_month_line = AbuTLine(benchmark_month.close, 'benchmark month line')
        # 计算这个月最少需要几次拟合才能代表走势曲线
        least = benchmark_month_line.show_least_valid_poly(show=False)

        if least >= self.poly:
            # 如果最少的拟合次数大于阀值self.poly，说明走势成立，大盘非震荡走势，解锁交易
            self.lock = False
        else:
            # 如果最少的拟合次数小于阀值self.poly，说明大盘处于震荡走势，封锁策略进行交易
            self.lock = True

    def fit_day(self, today):
        if self.lock:
            # 如果封锁策略进行交易的情况下，策略不进行择时
            return None

        # 今天的收盘价格达到xd天内最高价格则符合买入条件
        if today.close == self.xd_kl.close.max():
            return self.buy_tomorrow()

class AbuFactorSellBreak(AbuFactorSellXD):
    """示例继承AbuFactorBuyXD, 向下突破卖出择时因子"""
    def support_direction(self):
        """支持的方向，只支持正向"""
        return [ESupportDirection.DIRECTION_CAll.value]

    def fit_day(self, today, orders):
        """
        寻找向下突破作为策略卖出驱动event
        :param today: 当前驱动的交易日金融时间序列数据
        :param orders: 买入择时策略中生成的订单序列
        """
        # 今天的收盘价格达到xd天内最低价格则符合条件
        if today.close == self.xd_kl.close.min():
            for order in orders:
                self.sell_tomorrow(order)

def read_symbols():
    pass


def main():

    ## 读股票
    symbols = read_symbols()
    print("一共有多少个股票? %d" % len(symbols))

    # 设置初始资金数
    read_cash = 1000000
    # 设置选股因子，None为不使用选股因子
    stock_pickers = None
    # 买入因子依然延用向上突破因子
    buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
                   {'xd': 42, 'class': AbuFactorBuyBreak}]
    buy_factors = [ {'xd': 42, 'class': AbuFactorBuyBreak, 'position': {'class': AbuABinPosition}}]

    # 卖出因子继续使用上一节使用的因子
    sell_factors = [
        {'stop_loss_n': 1.0, 'stop_win_n': 3.0,
         'class': AbuFactorAtrNStop},
        {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.5},
        {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
    ]

    sell_factors = [ {'stop_loss_n': 1.0, 'stop_win_n': 20.0,  'class': AbuFactorAtrNStop}]
    #sell_factors = [ ]

    # 择时股票池
    # 使用run_loop_back运行策略


    
    # 买入因子依然延用向上突破因子
    buy_factors = [{'xd': 60, 'class': AbuSDBreak},
                   {'xd': 42, 'class': AbuSDBreak}]
    buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
                   {'xd': 42, 'class': AbuFactorBuyBreak}]
    # 卖出因子继续使用上一节使用的因子
    sell_factors = [
        {'stop_loss_n': 1.0, 'stop_win_n': 3.0,
         'class': AbuFactorAtrNStop},
        {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.5},
        {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
    ]

    choice_symbols = ['hk03333', 'hk00700', 'hk02333', 'hk01359', 'hk00656', 'hk03888', 'hk02318']
    choice_symbols = ['usNOAH', 'usSFUN', 'usBIDU', 'usAAPL', 'usGOOG', 'usTSLA', 'usWUBA', 'usVIPS']
    abupy.env.g_market_target = abupy.EMarketTargetType.E_MARKET_TARGET_HK
    abupy.env.g_market_target = abupy.EMarketTargetType.E_MARKET_TARGET_US
    abu_result_tuple, kl_pd_manger = abu.run_loop_back(read_cash,
                                                       buy_factors,
                                                       sell_factors,
                                                       stock_pickers,
                                                       choice_symbols=choice_symbols,
                                                       n_folds=6)
    ABuProgress.clear_output()

    metrics = AbuMetricsBase(*abu_result_tuple)
    metrics.fit_metrics()
    metrics.plot_returns_cmp()

    pd.set_option('display.expand_frame_repr', False)
    pd.options.display.max_rows = 999
if __name__ == '__main__':
    main()

# 第一个问题: 没有显示的banchmark, 那么banchmark是什么?
#   banchmark如果不指定, 是由一个全局变变控制的, 一般用这种方法设置:
# # 设置市场类型为港股
#    abupy.env.g_market_target = EMarketTargetType.E_MARKET_TARGET_HK
# 第二个问题: 如何知道并控制每次交易的数量?
#    这个问题的答案只能到AbuCapital类中去找.
#    初始化的时候给了capital_pd.cash_balance