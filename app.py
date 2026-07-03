"""エントリポイント（app.py）。

役割：
- アプリ全体の入口画面（ランディングページ）を表示する
- 各画面（pages/配下）への導線と、アプリの使い方を簡単に示す
- 個別のロジックは持たない（各担当のlogic/配下・pages/配下に実装がある）
"""

import streamlit as st

st.set_page_config(
    page_title="株価分析アプリ",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("株価分析アプリ")
st.caption("過去の値動きと現在の指標を比較し、投資判断の参考情報を提示するツール")

st.markdown(
    """
左のサイドバーから各画面に移動できます。まずは **「トップ」** で銘柄コードと
取得期間を指定し、データを取得してください。他の画面はこのデータを使って動きます。
"""
)

st.divider()
st.subheader("画面一覧")

pages_info = [
    ("トップ", "銘柄コード・期間の入力とデータ取得、基準日100正規化チャート"),
    ("サマリー", "取得結果の要約表示"),
    ("株価チャート", "株価の詳細チャート"),
    ("複数指標分析", "RSI・ボリンジャーバンド・HV・出来高倍率などの詳細"),
    ("過去類似局面", "現在の指標に近い過去の局面を抽出"),
    ("デモトレード結果", "類似局面を起点にしたデモ売買のシミュレーション結果"),
    ("補助判断", "例外・注意事項などの補助情報"),
]
for name, desc in pages_info:
    st.markdown(f"- **{name}**：{desc}")

st.divider()

ticker = st.session_state.get("selected_ticker")
if ticker:
    st.info(f"現在選択中の銘柄：{ticker}（トップ画面で変更できます）")
else:
    st.warning("まだ銘柄が選択されていません。「トップ」画面から始めてください。")