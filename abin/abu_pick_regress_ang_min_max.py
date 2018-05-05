
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
from abupy import AbuPickStockBase, ps, ABuRegUtil


"""
buPickRegressAngMinMax为选股因子，它的作用是将股票前期走势进行线性拟合计算一个角度，参数为选股条件，
将选股条件作用于角度后进行股票的筛选。
"""
class AbuPickRegressAngMinMax(AbuPickStockBase):
    """拟合角度选股因子示例类"""

    def _init_self(self, **kwargs):
        """通过kwargs设置拟合角度边际条件，配置因子参数"""

        # 暂时与base保持一致不使用kwargs.pop('a', default)方式
        # fit_pick中 ang > threshold_ang_min, 默认负无穷，即默认所有都符合
        self.threshold_ang_min = -np.inf
        if 'threshold_ang_min' in kwargs:
            # 设置最小角度阀值
            self.threshold_ang_min = kwargs['threshold_ang_min']

        # fit_pick中 ang < threshold_ang_max, 默认正无穷，即默认所有都符合
        self.threshold_ang_max = np.inf
        if 'threshold_ang_max' in kwargs:
            # 设置最大角度阀值
            self.threshold_ang_max = kwargs['threshold_ang_max']

    @ps.reversed_result
    def fit_pick(self, kl_pd, target_symbol):
        """开始根据自定义拟合角度边际参数进行选股"""
        # 计算走势角度
        ang = ABuRegUtil.calc_regress_deg(kl_pd.close, show=False)
        # 根据参数进行角度条件判断
        if self.threshold_ang_min < ang < self.threshold_ang_max:
            return True
        return False

    def fit_first_choice(self, pick_worker, choice_symbols, *args, **kwargs):
        raise NotImplementedError('AbuPickRegressAng fit_first_choice unsupported now!')