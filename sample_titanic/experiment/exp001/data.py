import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


class Dataset:

    TRAIN_CSV_PATH = "../../input/titanic/train.csv"
    TEST_CSV_PATH = "../../input/titanic/test.csv"

    COLUMNS = ["PassengerId", "Pclass", "Name", "Sex", "Age", "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"]
    TARGET_COLUMN = "Survived"

    def _age_complement(self, in_df: pd.DataFrame, seed: int = 24) -> tuple[pd.DataFrame, list[str]]:
        out_df = in_df.copy()

        # ワンホットエンコーディング
        data_df = out_df[["Age", "Pclass", "Sex", "Parch", "SibSp"]]
        data_df = pd.get_dummies(data_df)

        notnull_data = data_df[data_df["Age"].notnull()].values
        isnull_data = data_df[data_df["Age"].isnull()].values

        # 年齢推定モデル構築
        rf_regressor = RandomForestRegressor(random_state=seed, n_estimators=100, n_jobs=-1)
        rf_regressor.fit(notnull_data[:, 1:], notnull_data[:, 0])

        # 年齢推定
        predict_age = rf_regressor.predict(isnull_data[:, 1:])
        out_df.loc[out_df["Age"].isnull(), "Age"] = np.round(predict_age)
        return out_df


    def _fare_complement(self, in_df: pd.DataFrame) -> pd.DataFrame:
        out_df = in_df.copy()
        fare_median = out_df.loc[(out_df["Embarked"] == "S") & (out_df["Pclass"] == 3), "Fare"].median()
        out_df["Fare"] = out_df["Fare"].fillna(fare_median)
        return out_df


    def _embarked_complement(self, in_df: pd.DataFrame) -> pd.DataFrame:
        out_df = in_df.copy()
        out_df["Embarked"] = out_df["Embarked"].fillna("S")
        return out_df


    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        train_df = pd.read_csv(self.TRAIN_CSV_PATH)
        test_df = pd.read_csv(self.TEST_CSV_PATH)

        test_df["Survived"] = np.nan
        df = pd.concat([train_df, test_df], ignore_index=True, sort=False)

        df = self._age_complement(df)
        df = self._fare_complement(df)
        df = self._embarked_complement(df)

        train_df = df[df["Survived"].notnull()]
        test_df = df[df["Survived"].isnull()].drop("Survived", axis=1)

        return train_df, test_df
