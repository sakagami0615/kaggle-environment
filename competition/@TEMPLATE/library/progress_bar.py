from collections.abc import Callable

from tqdm import tqdm as tqdm_terminal
from tqdm.notebook import tqdm as tqdm_notebook


def get_tqdm() -> type:
    try:
        # Jupyter Notebook / IPython かどうかを判定
        from IPython import get_ipython

        shell = get_ipython()
        if shell and shell.__class__.__name__ in ["ZMQInteractiveShell"]:
            return tqdm_notebook  # Jupyter notebook/lab
    except Exception:  # noqa
        pass
    return tqdm_terminal  # 通常ターミナル


tqdm = get_tqdm()


class ProgressBar:
    def __init__(self, n_trials=None):
        self._n_trials = n_trials
        self._bar = None

    @property
    def n_trials(self) -> int:
        return self._n_trials

    @n_trials.setter
    def n_trials(self, n_trials: int) -> None:
        self._n_trials = n_trials

    def process(self) -> None:
        if self._bar is None:
            self._bar = tqdm(total=self._n_trials)
        elif self._bar.n >= self.n_trials:
            self._bar.close()
            self._bar = tqdm(total=self._n_trials)
        self._bar.update(1)

    def decorate(self, func) -> Callable:
        def wrapper(*args, **kwargs):
            if self.n_trials:
                self.process()
            result = func(*args, **kwargs)
            return result

        return wrapper
