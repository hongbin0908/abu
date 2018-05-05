from __future__ import print_function
from __future__ import division

import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import os
import sys
import numpy as np
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('.'))
import abupy

def main():
    #是否使用测试
    abupy.env.enable_example_env_ipython()
    # 设置初始资金数
    read_cash = 1000000
    # 设置选股因子，None为不使用选股因子

    stop_win_range = np.arange(2.0, 4.5, 0.5)
    stop_loss_range = np.arange(0.5, 2, 0.5)

    abu_atr_nstop_grid = {
        'class': [abupy.AbuFactorAtrNStop],
        'stop_loss_n': stop_loss_range,
        'stop_win_n': stop_win_range,
    }





    
if __name__ == '__main__':
    main()





