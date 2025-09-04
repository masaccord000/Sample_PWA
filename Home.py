import streamlit as st
import base64

def get_base64_image(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def render():
    image_base64 = get_base64_image("icon.png")
    st.markdown(
        f"""
        <style>
        .custom-logo {{
            height: 3em;
            margin-right: 0.5em;
            filter: drop-shadow(0 0 6px white);
        }}
        </style>
        <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{image_base64}" class="custom-logo">
            <h2 style="margin: 0;">変電アプリ</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("これは stlite で構築されたホームページです。")
