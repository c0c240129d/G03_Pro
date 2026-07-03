"""相川担当：補助判断表示画面（pages/7_decision_support.py）

サマリー画面のタブから遷移する詳細画面という位置づけ。
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from logic.csv_export import save_csv
from logic.error_utils import show_error, show_warning

st.title("補助判断")

# --- ダミーデータ ---------------------------------------------------------
# 岩間さんのcalc_demo_trade()がマージされたら、この仮置きデータを
# st.session_state経由で受け取った本物のDataFrameに差し替える。
# カラム構成はcalc_demo_tradeの出力仕様（Action, Horizon, AvgReturn, WinRate,
# MaxLoss, MaxDrawdown, AvgHoldDays）に合わせてある。
dummy_result_df = pd.DataFrame(
    {
        "Action": ["buy", "buy", "buy", "sell", "sell", "sell"],
        "Horizon": [5, 10, 20, 5, 10, 20],
        "AvgReturn": [0.021, 0.033, 0.045, -0.008, 0.004, 0.012],
        "WinRate": [0.62, 0.60, 0.58, 0.41, 0.47, 0.53],
        "MaxLoss": [-0.05, -0.07, -0.09, -0.11, -0.09, -0.07],
        "MaxDrawdown": [-0.03, -0.05, -0.07, -0.09, -0.07, -0.05],
        "AvgHoldDays": [5.0, 10.0, 20.0, 5.0, 10.0, 20.0],
    }
)

result_df = dummy_result_df

if result_df is None or result_df.empty:
    show_error("表示できる分析結果がありません。")
    st.stop()

# --- 補助判断のハイライト表示 ---------------------------------------------
st.subheader("補助判断")

best_row = result_df.loc[result_df["AvgReturn"].idxmax()]
st.success(
    f"過去類似局面では「{best_row['Action']}（保有{int(best_row['Horizon'])}日）」が"
    f"比較的良い結果となっています"
    f"（平均リターン {best_row['AvgReturn']:.2%} / 勝率 {best_row['WinRate']:.0%}）。"
)

# --- 各投資行動の結果を根拠として表示 ---------------------------------------
st.subheader("各投資行動の結果")
for _, row in result_df.iterrows():
    st.info(
        f"{row['Action']}（保有{int(row['Horizon'])}日）: "
        f"平均リターン {row['AvgReturn']:.2%} / 勝率 {row['WinRate']:.0%} / "
        f"最大損失 {row['MaxLoss']:.2%} / 最大ドローダウン {row['MaxDrawdown']:.2%} / "
        f"平均保有日数 {row['AvgHoldDays']:.1f}日"
    )

# --- 注意事項 ---------------------------------------------------------
st.warning("本結果は将来の利益を保証するものではありません。また、手数料・税金は考慮していません。")


# --- CSVエクスポート ----------------------------------------------------
def _on_export_click() -> None:
    """ダウンロードボタン押下時にサーバー側へもCSVを保存し、結果をsession_stateへ記録する。"""
    ok = save_csv(result_df, "decision_support_result.csv")
    st.session_state["decision_support_export_success"] = ok


st.download_button(
    label="分析結果をCSVで保存",
    data=result_df.to_csv(index=False).encode("utf-8-sig"),
    file_name="decision_support_result.csv",
    mime="text/csv",
    on_click=_on_export_click,
)

export_success = st.session_state.get("decision_support_export_success")
if export_success is False:
    show_error("CSVの保存に失敗しました。")
