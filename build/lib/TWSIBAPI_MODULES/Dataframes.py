import pandas as pd
from ibapi.common import BarData
from typing import List


def ohlcv_dataframe(bars: List[BarData]) -> pd.DataFrame:
    df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    for bar in bars:
        ser = pd.Series([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume], index=df.columns)
        df = df.append(ser, ignore_index=True)
    return df


def append_bar(df: pd.DataFrame, bars: List[BarData]) -> pd.DataFrame:
    for bar in bars:
        ser = pd.Series([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume], index=df.columns)
        df = df.append(ser, ignore_index=True)
    return df
