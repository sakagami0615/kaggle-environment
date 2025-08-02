import math
import sys
from collections.abc import Iterator

import pandas as pd


class SlideWindowTimeSeriesSplit:
    """
    時系列データをスライディングウィンドウ方式で分割するためのクラス。

    各分割では、時系列の順序を保ちながらトレーニングとテストの期間を交互にずらして生成される。
    トレーニングとテストのサイズは `train_ratio` に基づいて決定され、全体を均等に分割する。

    Parameters:
        timeseries_column (str): ソート・分割に使用する時系列カラムの列名。
        n_splits (int): 分割数。デフォルトは5。
        train_ratio (float): トレーニングデータの割合（0 < train_ratio < 1）。デフォルトは0.7。

    Raises:
        ValueError: train_ratio が 0 未満または 1 を超える場合。
    """

    def __init__(self, timeseries_column: str, n_splits: int = 5, train_ratio: float = 0.7):
        if self._is_less(train_ratio, 0) or self._is_greater(train_ratio, 1):
            raise ValueError("train_ratio must be a real number between 0 and 1")

        self._timeseries_column = timeseries_column
        self._n_splits = n_splits
        self._train_ratio = train_ratio
        self._test_ratio = 1.0 - train_ratio

    def _is_less(self, a: float, b: float) -> bool:
        return (a - b) < sys.float_info.epsilon

    def _is_greater(self, a: float, b: float) -> bool:
        return (a - b) >= sys.float_info.epsilon

    def split(self, X: pd.DataFrame) -> Iterator[tuple[pd.RangeIndex, pd.RangeIndex]]:
        """
        入力された時系列 DataFrame を `n_splits` 分割し、スライディングウィンドウでトレーニング／テストのインデックスを生成する。

        時系列カラムで昇順ソートされたデータに対して、各スプリットで重複のないように
        トレーニング／テストの期間を順にずらして出力する。

        Parameters:
            X (pd.DataFrame): 対象の時系列データ。`timeseries_column` を含む必要がある。

        Yields:
            Iterator[tuple[pd.RangeIndex, pd.RangeIndex]]: 
                トレーニングとテストに使用するインデックスのタプル。各スプリットごとに順に yield される。
        """
        # ソートした時系列データを取得
        date_series = X[self._timeseries_column]
        date_series = date_series.reset_index()
        date_series = date_series.sort_values(by=self._timeseries_column)
        date_series = date_series[self._timeseries_column]

        n_dates = len(date_series)

        ratio = self._train_ratio * self._n_splits + self._test_ratio
        n_train_elems = math.floor(n_dates / ratio * self._train_ratio)
        n_test_elems = n_dates - n_train_elems * self._n_splits

        for i in range(self._n_splits):
            train_begin_idx = i * n_train_elems
            train_end_idx = train_begin_idx + n_train_elems - 1
            test_begin_idx = train_end_idx + 1
            test_end_idx = test_begin_idx + n_test_elems - 1

            train_begin = date_series.iloc[train_begin_idx]
            train_end = date_series.iloc[train_end_idx]
            test_begin = date_series.iloc[test_begin_idx]
            test_end = date_series.iloc[test_end_idx]

            train_iloc_index = X[(train_begin <= date_series) & (date_series <= train_end)].index
            test_iloc_index = X[(test_begin <= date_series) & (date_series <= test_end)].index

            yield train_iloc_index, test_iloc_index
