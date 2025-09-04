import streamlit as st
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="画像一括リサイズ", layout="centered")

st.title("📐 画像一括リサイズアプリ")

# リサイズ方法の選択
resize_mode = st.selectbox("リサイズ方法を選択", [
    "縮小率（%）",
    "高さ（px）",
    "幅（px）",
    "長辺（px）",
    "短辺（px）"
])

# パラメータ入力
if resize_mode == "縮小率（%）":
    scale_percent = st.selectbox("縮小率を選択", list(range(10, 110, 10)), index=4)
elif resize_mode == "高さ（px）":
    target_height = st.selectbox("高さを選択", list(range(100, 1100, 100)), index=4)
elif resize_mode == "幅（px）":
    target_width = st.selectbox("幅を選択", list(range(100, 1100, 100)), index=4)
elif resize_mode == "長辺（px）":
    target_long = st.selectbox("長辺を選択", list(range(100, 2100, 100)), index=9)
elif resize_mode == "短辺（px）":
    target_short = st.selectbox("短辺を選択", list(range(100, 1100, 100)), index=4)

# 🔘 結果をクリアボタン（設定UIの直下）
if st.button("🧹 結果をクリア"):
    st.session_state.uploaded_files = None
    st.experimental_rerun()

# ファイルアップロード
uploaded_files = st.file_uploader("画像ファイルを複数選択", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# リサイズ処理
if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            original_size = image.size

            # リサイズ処理
            if resize_mode == "縮小率（%）":
                new_size = (int(original_size[0] * scale_percent / 100),
                            int(original_size[1] * scale_percent / 100))
            elif resize_mode == "高さ（px）":
                ratio = target_height / original_size[1]
                new_size = (int(original_size[0] * ratio), target_height)
            elif resize_mode == "幅（px）":
                ratio = target_width / original_size[0]
                new_size = (target_width, int(original_size[1] * ratio))
            elif resize_mode == "長辺（px）":
                long_side = max(original_size)
                ratio = target_long / long_side
                new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
            elif resize_mode == "短辺（px）":
                short_side = min(original_size)
                ratio = target_short / short_side
                new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))

            resized_image = image.resize(new_size, Image.LANCZOS)

            # 表示
            st.image(resized_image, caption=f"{uploaded_file.name} → {new_size}", use_column_width=True)

            # ZIPに追加
            img_bytes = io.BytesIO()
            resized_image.save(img_bytes, format="PNG")
            zip_file.writestr(f"resized_{uploaded_file.name}", img_bytes.getvalue())

    # ZIPダウンロード
    st.download_button(
        label="📦 ZIPで一括ダウンロード",
        data=zip_buffer.getvalue(),
        file_name="resized_images.zip",
        mime="application/zip"
    )
