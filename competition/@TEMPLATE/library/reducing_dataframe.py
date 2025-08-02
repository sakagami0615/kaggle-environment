import numpy as np
import pandas as pd


def reduce_mem_usage(props: pd.DataFrame, verbose: bool = False) -> tuple[pd.DataFrame, list]:
    """
    DataFrameの各列のデータ型を最適化してメモリ使用量を削減する。

    数値列に対して最小限の整数型または `float32` に変換を試み、
    メモリ使用量を大幅に削減することができる。欠損値のある列には
    最小値-1を補完し、補完された列名はリストとして返す。

    Parameters
    ----------
    props : pd.DataFrame
        メモリ使用量を削減したい対象のDataFrame。
    verbose : bool, default False
        各列ごとの変換前後のdtypeやメモリ使用量を詳細に出力するかどうか。

    Returns
    -------
    tuple
        - pd.DataFrame : データ型が変換された新しいDataFrame。
        - list : 欠損値を補完した列の名前のリスト。

    Notes
    -----
    - オブジェクト型（文字列など）は対象外。
    - 欠損値のある列は `min - 1` で一時的に埋められる。
    - 元のDataFrameをインプレースで変更する（新しいオブジェクトは返さない）。
    - 浮動小数点型は `float32` に変換される。

    Examples
    --------
    >>> reduced_df, na_columns = reduce_mem_usage(df, verbose=True)
    Memory usage of properties dataframe is :  64.0  MB
    Column:  price
    dtype before:  float64
    dtype after:  float32
    ...
    This is 23.5% of the initial size
    """
    start_mem_usg = props.memory_usage().sum() / 1024**2

    if verbose:
        print("Memory usage of properties dataframe is :", start_mem_usg, " MB")

    na_list = []  # Keeps track of columns that have missing values filled in.
    for col in props.columns:
        if props[col].dtype != object:  # Exclude strings
            if verbose:
                # Print current column type
                print("******************************")
                print("Column: ", col)
                print("dtype before: ", props[col].dtype)

            # make variables for Int, max and min
            IsInt = False
            mx = props[col].max()
            mn = props[col].min()

            # Integer does not support NA, therefore, NA needs to be filled
            if not np.isfinite(props[col]).all():
                na_list.append(col)
                props[col].fillna(mn - 1, inplace=True)

            # test if column can be converted to an integer
            asint = props[col].fillna(0).astype(np.int64)
            result = props[col] - asint
            result = result.sum()
            if result > -0.01 and result < 0.01:
                IsInt = True

            # Make Integer/unsigned Integer datatypes
            if IsInt:
                if mn >= 0:
                    if mx < 255:
                        props[col] = props[col].astype(np.uint8)
                    elif mx < 65535:
                        props[col] = props[col].astype(np.uint16)
                    elif mx < 4294967295:
                        props[col] = props[col].astype(np.uint32)
                    else:
                        props[col] = props[col].astype(np.uint64)
                else:
                    if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                        props[col] = props[col].astype(np.int8)
                    elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                        props[col] = props[col].astype(np.int16)
                    elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                        props[col] = props[col].astype(np.int32)
                    elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                        props[col] = props[col].astype(np.int64)

            # Make float datatypes 32 bit
            else:
                props[col] = props[col].astype(np.float32)

            if verbose:
                # Print new column type
                print("dtype after: ", props[col].dtype)
                print("******************************")

    # Print final result
    if verbose:
        mem_usg = props.memory_usage().sum() / 1024**2
        print("___MEMORY USAGE AFTER COMPLETION:___")
        print("Memory usage is: ", mem_usg, " MB")
        print("This is ", 100 * mem_usg / start_mem_usg, "% of the initial size")

    return props, na_list
