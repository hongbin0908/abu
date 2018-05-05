from __future__ import print_function
from __future__ import division

import warnings

from abupy.TLineBu.ABuTLine import AbuTLine

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import os
import sys
sys.path.insert(0, os.path.abspath('../'))
import abupy

# configure begin
ONLY_TEST = True
# configure end

markets = [abupy.EMarketTargetType.E_MARKET_TARGET_CN, abupy.EMarketTargetType.E_MARKET_TARGET_US, abupy.EMarketTargetType.E_MARKET_TARGET_HK]
def main():
    abupy.env.g_market_source = abupy.EMarketSourceType.E_MARKET_SOURCE_tx
    for e in markets:
        if not ONLY_TEST:
            abupy.abu.run_kl_update(n_folds=20, market=e, n_jobs= 1, how='thread')

    print("股票下载情况:")
    for e in markets:
        total = 0
        valid = 0
        symbols = abupy.ABuMarket.all_symbol()
        abupy.env.g_data_fetch_mode = abupy.EMarketDataFetchMode.E_DATA_FETCH_FORCE_LOCAL
        for symbol in symbols:
            total += 1
            if (total % 100) == 0:
                print('total: %d' % total)
            df = abupy.ABuSymbolPd.make_kl_df(symbol);
            if type(df) == type(None):
                pass
            else:
                valid += 1
        print('%s total: %d, valid %d (%.2f%%)' % (e, total, valid, valid*.10/total))

if __name__ == '__main__':
    main()
