"""相川担当：CSV保存処理（logic/csv_export.py）"""

from __future__ import annotations

import pandas as pd


def save_csv(df: pd.DataFrame, filename: str) -> bool:
    """DataFrameをCSVファイルとして保存し、成功時True・失敗時Falseを返す（UI処理は行わない）。"""
    try:
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        return True
    except Exception:
        return False
