# Kaggle Environment

Kaggle公式のDockerイメージを使用した機械学習の実験環境。  
JupyterLabとMLflowを統合し、再現性の高い実験管理を実現。

## Features

- Kaggle公式Dockerイメージ（`gcr.io/kaggle-gpu-images/python`）を使用
- JupyterLabによる対話的な開発環境
- MLflowによる実験管理とトラッキング
- GPU対応
- Kaggle APIによるデータセットのダウンロードと結果の提出

## Project Structure

```
.
├── config/
│   ├── kaggle.json.sample      # Kaggle API認証情報のサンプル
│   └── kaggle.json             # Kaggle API認証情報（gitignore対象）
│
└── sample_titanic/             # コンペティションごとのプロジェクト(tittanicコンペを例に作成したもの)
    ├── docker/
    │   ├── docker-compose.yml  # Docker Compose設定
    │   ├── .env.sample         # 環境変数のサンプル
    │   └── mlflow/
    │       └── Dockerfile      # MLflow用Dockerfile
    ├── experiment/             # 実験コード（/kaggle/workingにマウント）
    │   └── exp001/
    │       ├── config.yml      # モデルパラメータ設定
    │       ├── data.py         # データローダー
    │       ├── train.py        # 学習スクリプト
    │       ├── util.py         # ユーティリティ関数
    │       └── eda.ipynb       # 探索的データ分析ノートブック
    ├── input/                  # データセット
    ├── result/                 # 提出ファイル
    ├── artifact/               # MLflowk関連のファイル群
    │   └── mlruns/
    └── log/
        └── score.md            # 実験結果スコア管理
```

## Setup

### 1. Kaggle API認証情報の設定

Kaggle APIを使用するための認証情報を設定します。

```bash
# kaggle.json.sampleをコピー
cp config/kaggle.json.sample config/kaggle.json

# 認証情報を編集
vi config/kaggle.json
```

`config/kaggle.json`に以下の形式でKaggleのユーザー名とAPIキーを設定してください：

```json
{"username":"your_kaggle_username","key":"your_kaggle_api_key"}
```

Kaggle APIキーは、[Kaggleアカウント設定](https://www.kaggle.com/settings/account)の「API」セクションから取得できます。

### 2. 環境変数の設定

```bash
cd sample_titanic/docker
cp .env.sample .env
```

必要に応じて`.env`ファイルを編集してください。

### 3. Docker環境の起動

```bash
cd sample_titanic/docker
docker-compose up -d
```

以下のサービスが起動します：
- JupyterLab: http://localhost:8888
- MLflow UI: http://localhost:5000

> **[NOTE]**  
> ポート番号は、.env で設定した値となる。

## Usage

以下の内容は、サンプルとして用意した `sample_titanic` の Usage となる。  

### データセットのダウンロード

コンテナ内でKaggle CLIを使用してデータセットをダウンロードします。

```bash
# コンテナに入る
docker exec -it sample_titanic_kaggle bash

# データセットをダウンロード
cd /kaggle/input
kaggle competitions download -c titanic
unzip titanic.zip
```

> **[NOTE]**  
> コンテナ名は、.env で設定した値となる。

### 実験の実行

実験は`experiment/`ディレクトリ内で管理します。各実験ごとにディレクトリを作成します。

```bash
# コンテナ内で実行
cd /kaggle/working/exp001
python train.py
```

### 結果の提出

```bash
# コンテナ内で実行
COMPE_NAME=titanic
EXP_NAME=exp001
SUBMIT_CSV_PATH=/kaggle/result/${EXP_NAME}/submission.csv

kaggle competitions submit -c ${COMPE_NAME} -f ${SUBMIT_CSV_PATH} -m "experiment message"
```

### スコア管理

実験結果は`log/score.md`に記録します。Pythonから読み込むこともできます。

```python
from util import load_score_md

df = load_score_md("/kaggle/log/score.md")
print(df)
```

## Environment Variables

`.env`ファイルで以下の環境変数を設定できます：

| 変数名 | 説明 | デフォルト値 |
| --- | --- | --- |
| KAGGLE_CONTAINER_NAME | Kaggleコンテナ名 | sample_titanic_kaggle |
| MLFLOW_CONTAINER_NAME | MLflowコンテナ名 | sample_titanic_mlflow |
| INPUT_FOLDER | データセットフォルダ | ../input |
| WORKING_FOLDER | 作業フォルダ | ../experiment |
| RESULT_FOLDER | 結果フォルダ | ../result |
| MLRUNS_FOLDER | MLflow成果物フォルダ | ../artifact/mlruns |
| LOG_FOLDER | ログフォルダ | ../log |
| PYTORCH_CONTAINER_SHM_SIZE | 共有メモリサイズ | 8gb |
| JUPYTER_PORT | JupyterLabポート | 8888 |
| MLFLOW_PORT | MLflowポート | 5000 |

## Tips

### 新しいコンペティション用プロジェクトの作成

`sample_titanic/`をコピーして新しいプロジェクトを作成します。

```bash
cp -r sample_titanic/ sample_newcompetition/
cd sample_newcompetition/docker
vi .env  # コンテナ名などを変更
docker-compose up -d
```

### コンテナのシェルに入る

```bash
docker exec -it sample_titanic_kaggle bash
```

### コンテナの停止

```bash
cd sample_titanic/docker
docker-compose down
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
