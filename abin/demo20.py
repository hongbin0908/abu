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

# 初始化资金500万
read_cash = 5000000

# 买入因子依然延用向上突破因子
buy_factors = [{'xd': 60, 'class': abupy.AbuFactorBuyBreak},
               {'xd': 42, 'class': abupy.AbuFactorBuyBreak}]

# 卖出因子继续使用上一节使用的因子
sell_factors = [
    {'stop_loss_n': 1.0, 'stop_win_n': 3.0,
     'class': abupy.AbuFactorAtrNStop},
    {'class': abupy.AbuFactorPreAtrNStop, 'pre_atr_n': 1.5},
    {'class': abupy.AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
]

def run_loop_back():
    global abu_result_tuple
    abu_result_tuple, _ = abupy.abu.run_loop_back(read_cash,
                                            buy_factors,
                                            sell_factors,
                                            choice_symbols=None,
                                            start='2012-08-08', end='2017-08-08')
    # 把运行的结果保存在本地，以便之后分析回测使用，保存回测结果数据代码如下所示
    abupy.abu.store_abu_result_tuple(abu_result_tuple, n_folds=5, store_type=abupy.EStoreAbu.E_STORE_CUSTOM_NAME,
                               custom_name='train_cn')
    abupy.ABuProgress.clear_output()

def run_load_train():
    global abu_result_tuple
    abu_result_tuple = abupy.abu.load_abu_result_tuple(n_folds=5, store_type=abupy.EStoreAbu.E_STORE_CUSTOM_NAME,
                                                 custom_name='train_cn')

def main():

    abupy.env.g_market_target = abupy.EMarketTargetType.E_MARKET_TARGET_CN
    abupy.env.g_data_fetch_mode = abupy.EMarketDataFetchMode.E_DATA_FETCH_FORCE_LOCAL

    # 回测生成买入时刻特征
    abupy.env.g_enable_ml_feature = True
    # 回测开始时将symbols切割分为训练集数据和测试集两份，使用训练集进行回测
    abupy.env.g_enable_train_test_split = True

    abupy.feature.clear_user_feature()
    abupy.feature.append_user_feature(abupy.AbuFeatureDegExtend)

    abu_result_tuple = None

    run_loop_back()


if __name__ == '__main__':
    main()

