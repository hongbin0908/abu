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

#是否使用测试
abupy.env.enable_example_env_ipython()
from abin.abu_pick_regress_ang_min_max import AbuPickRegressAngMinMax
from abin.AbuPickStockPriceMinMax import AbuPickStockPriceMinMax

def main():
    stock_picks = [
        {'class': AbuPickRegressAngMinMax,
         'threshold_ang_min':0.0,
         'threshold_ang_max':100.0,
         'xd': 365,
         'min_xd': 100,
         'reversed':False},
        {'class': AbuPickStockPriceMinMax,
         'threshold_price_min':50.0,
         'threshold_price_max':1000.0,
         'xd': 365,
         'min_xd': 100,
         'reversed':False}
    ]

    choice_symbols = ['usNOAH', 'usSFUN', 'usBIDU', 'usAAPL', 'usGOOG',
                      'usTSLA', 'usWUBA', 'usVIPS']

    benchmark = abupy.AbuBenchmark()
    capital = abupy.AbuCapital(1000000, benchmark)
    kl_pd_manager = abupy.AbuKLManager(benchmark, capital)
    selected = abupy.ABuPickStockExecute.do_pick_stock_work(capital=capital,
                                                 benchmark=benchmark,
                                                 choice_symbols=choice_symbols,
                                                 stock_pickers=stock_picks)
    #stock_picker = abupy.AbuPickStockWorker(capital, benchmark, kl_pd_manager, choice_symbols = choice_symbols, stock_pickers=stock_picks)
    #stock_picker.fit()
    print(selected)

    #kl_pd_noah = kl_pd_manager.get_pick_stock_kl_pd('usNOAH')
    #deg = abupy.ABuRegUtil.calc_regress_deg(kl_pd_noah.close)
    #print('noah 选股周期内角度={}'.format(round(deg, 3)))

if __name__ == '__main__':
    main()





