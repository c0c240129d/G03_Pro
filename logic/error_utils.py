"""相川担当：例外対応共通モジュール（logic/error_utils.py）"""

from __future__ import annotations

import streamlit as st


def show_error(msg: str) -> None:
    """エラーメッセージ文字列を受け取り、st.error()で画面に表示する（返り値なし）。"""
    st.error(msg)


def show_warning(msg: str) -> None:
    """警告メッセージ文字列を受け取り、st.warning()で画面に表示する（返り値なし）。"""
    st.warning(msg)
