import os
import yaml
import pandas as pd


def load_config(file_path: str) -> dict:
    with open(file_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def get_exp_name() -> str:
    return os.path.basename(os.getcwd())


def load_score_md(file_path: str) -> pd.DataFrame:
    """
    Load score.md file as a pandas DataFrame.

    Args:
        file_path: Path to the score.md file

    Returns:
        DataFrame with columns: exp_name, CV, LB
    """
    df = pd.read_csv(file_path, sep="|", skiprows=1, skipinitialspace=True)
    # Remove empty columns at the beginning and end, Remove separator row (contains '---')
    df = df.iloc[1:, 1:-1].reset_index(drop=True)
    # Clean whitespace from column names and values
    df.columns = df.columns.str.strip()
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    # Convert CV and LB to float
    df['CV'] = pd.to_numeric(df['CV'], errors="coerce")
    df['LB'] = pd.to_numeric(df['LB'], errors="coerce")

    return df
