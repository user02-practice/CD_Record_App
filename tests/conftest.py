import tkinter as tk
import pytest


@pytest.fixture(scope="session")
def tk_root():
    """
    GUIテスト全体で使用するTkinterのルートウィンドウ。

    テストごとにTk()を作成すると、
    Tcl/Tkの初期化が不安定になることがあるため、
    テストセッション中は1つのrootを共有する。
    """

    root = tk.Tk()

    yield root

    root.destroy()