import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class PCA_wrapper(object):

    @staticmethod
    def get_label(pca):
        return ["PC{}".format(x + 1) for x in range(pca.n_components_)]

    @staticmethod
    def create_std_scaler(df):
        std_scaler = StandardScaler()
        std_scaler.fit(df)
        return std_scaler

    @staticmethod
    def create_pca(x_data):
        pca = PCA()
        pca.fit(x_data)
        return pca

    @staticmethod
    def create_decomposition(df, remove_columns=None):
        src_df = df.copy()
        if remove_columns is not None:
            src_df.drop(remove_columns, axis=1, inplace=True)

        std_scaler = PCA_wrapper.create_std_scaler(src_df)
        std_x_src = std_scaler.transform(src_df)
        pca = PCA_wrapper.create_pca(std_x_src)
        return std_scaler, pca

    @staticmethod
    def dimension_compression(std_scaler, pca, df, remove_columns=None):
        src_df = df.copy()
        if remove_columns is not None:
            src_df.drop(remove_columns, axis=1, inplace=True)

        pca_feature = pca.transform(std_scaler.transform(src_df))

        pca_columns = PCA_wrapper.get_label(pca)
        pca_df = pd.DataFrame(pca_feature, columns=pca_columns)
        return pca_df

    @staticmethod
    def get_feature_importance(pca):
        pca_columns = PCA_wrapper.get_label(pca)
        importance_df = pd.DataFrame(pca.explained_variance_ratio_, index=pca_columns, columns=["importance"])

        plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
        plt.plot([0] + list(np.cumsum(importance_df["importance"])), "-o")
        plt.xlabel("Number of principal components")
        plt.ylabel("Cumulative contribution rate")
        plt.grid()
        plt.show()
        return importance_df

    @staticmethod
    def get_eigenvalue(pca):
        pca_columns = PCA_wrapper.get_label(pca)
        return pd.DataFrame(pca.explained_variance_, index=pca_columns)

    @staticmethod
    def plot_2d(pca, pca_df, figsize=(6, 6), is_label=True):
        plt.figure(figsize=figsize)
        if is_label:
            for x, y, name in zip(pca.components_[0], pca.components_[1], pca_df.columns[1:]):
                plt.text(x, y, name)
        plt.scatter(pca.components_[0], pca.components_[1], alpha=0.8)
        plt.grid()
        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.show()
