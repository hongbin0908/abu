from __future__ import print_function
from __future__ import division

import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import os
import sys
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('.'))
import abupy

def main():
    #是否使用测试
    abupy.env.enable_example_env_ipython()
    # 设置初始资金数
    read_cash = 1000000
    # 设置选股因子，None为不使用选股因子
    stock_pickers = None
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
    # 择时股票池
    choice_symbols = ['usNOAH', 'usSFUN', 'usBIDU', 'usAAPL', 'usGOOG',
                      'usTSLA', 'usWUBA', 'usVIPS']
    # 使用run_loop_back运行策略
    abu_result_tuple, kl_pd_manger = abupy.abu.run_loop_back(read_cash,
                                                       buy_factors,
                                                       sell_factors,
                                                       stock_pickers,
                                                       choice_symbols=choice_symbols,
                                                       n_folds=2)
    abupy.ABuProgress.clear_output()

    #度量的基本使用方法
    #如上help信息所示，abu_result_tuple类型为AbuResultTuple对象，AbuMetricsBase类为abupy对回测结果进行度量的基础类，对于基于股票类型的 市场进行的回测可以直接使用，对于其它市场度量类有自己的专属类，如AbuMetricsFutures为对期货进行度量时使用，后面的章节示例期货回测时会示例使用。
    #首先通过AbuMetricsBase的参数进行结果度量，如下所示：
    #输出的文字信息打印了胜率、获利期望、亏损期望、策略收益、买入成交比例等信息
    #第一图为策略收益与基准收益对照
    #第二图为策略收益线性拟合曲线
    #第三图为策略收益资金概率密度图
    metrics = abupy.AbuMetricsBase(*abu_result_tuple)
    metrics.fit_metrics()
    metrics.plot_returns_cmp()

    # 可视化策略与基准之间波动率和夏普比率关系
    metrics.plot_sharp_volatility_cmp()

    # 可视化策略买入因子生效间隔天数， 统计买入因子的生效间隔，如图9-3所示。
    # 不同的类型的买入因子策略在生效周期上差别很大，组合不同特性的买入因子组
    # 成良好的买入策略很重要，但是要注意买入因子的组合不是组合的因子越多，
    # 优势越大，所有因子的组合、不光是优势的组合，同时也是劣势的组合。
    metrics.plot_effect_mean_day()

    # 可视化策略持股天数
    metrics.plot_keep_days()

    # 可视化策略卖出因子生效分布情况
    metrics.plot_sell_factors()

    # 函数中实现了计算最大回撤并可视化
    metrics.plot_max_draw_down()


if __name__ == '__main__':
    main()





