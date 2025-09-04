import streamlit as st
import Home
import About
import ResizeImages

st.set_page_config(page_title="変電アプリ", layout="centered")

# ドロップダウン形式のページ選択
page = st.sidebar.selectbox("ページを選択", ["Home", "画像一括リサイズ", "About"])

# ページ切り替え
if page == "Home":
    Home.render()
elif page == "About":
    About.render()
elif page == "画像一括リサイズ":
    ResizeImages.render()

