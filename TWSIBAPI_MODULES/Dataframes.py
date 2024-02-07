import pandas as pd
from ibapi.common import BarData
from typing import List


def ohlcv_dataframe(bars: List[BarData]) -> pd.DataFrame:
    """
    This function is used to create a dataframe from a list of BarData objects.
    :param bars: List of bar data objects retrieved from TWS or through a DataStreams function
    :return: Pandas dataframe with columns 'date', 'open', 'high', 'low', 'close', 'volume'
    """
    df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    for bar in bars:
        ser = pd.Series([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume], index=df.columns)
        df = df.append(ser, ignore_index=True)
    return df


def append_bar(df: pd.DataFrame, bars: List[BarData]) -> pd.DataFrame:
    """
    This function is used to append a bar to a dataframe.
    :param df: Pandas dataframe to append bar to
    :param bars: List of bars to append
    :return: Returns the dataframe with the appended bars
    """
    for bar in bars:
        ser = pd.Series([bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume], index=df.columns)
        df = df.append(ser, ignore_index=True)
    return df
