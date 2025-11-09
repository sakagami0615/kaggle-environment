import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

from data import Dataset
from util import get_exp_name, load_config


def onehot_encoding(train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    test_df[Dataset.TARGET_COLUMN] = np.nan
    df = pd.concat([train_df, test_df], ignore_index=True, sort=False)

    all_columns = [Dataset.TARGET_COLUMN] + Dataset.COLUMNS
    df = pd.get_dummies(df[all_columns])

    train_df = df[df[Dataset.TARGET_COLUMN].notnull()]
    test_df = df[df[Dataset.TARGET_COLUMN].isnull()].drop(Dataset.TARGET_COLUMN, axis=1)

    return train_df, test_df


def train(config: dict, train_df: pd.DataFrame) -> RandomForestClassifier:
    x = train_df.values[:, 1:]
    y = train_df.values[:, 0].astype(np.int32)

    clf = RandomForestClassifier(**config)
    clf.fit(x, y)

    cv_result = cross_validate(clf, x, y, cv= 10)
    print('mean_score = ', np.mean(cv_result['test_score']))
    print('mean_std = ', np.std(cv_result['test_score']))

    return clf


def predict(clf: RandomForestClassifier, test_df: pd.DataFrame):
    x = test_df.values
    preds = clf.predict(x)
    return preds


def create_submit_csv(preds: np.array, test_df: pd.DataFrame):
    exp_name = get_exp_name()
    result_dirpath = os.path.join("/kaggle/result", exp_name)
    os.makedirs(result_dirpath, exist_ok=True)

    submission = pd.DataFrame({
        "PassengerId": test_df["PassengerId"],
        "Survived": preds.astype(np.int32)
    })

    submit_csv_path = os.path.join(result_dirpath, "submission.csv")
    submission.to_csv(submit_csv_path, index=False)
    print(f"save submit csv: {submit_csv_path}")


def main():
    config = load_config("config.yml")

    train_df, test_df = Dataset().load_data()
    train_df, test_df = onehot_encoding(train_df, test_df)

    clf = train(config["train"]["model"]["rf"], train_df)

    test_preds = predict(clf, test_df)

    create_submit_csv(test_preds, test_df)



if __name__ == "__main__":
    main()
