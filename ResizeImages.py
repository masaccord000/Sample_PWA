import streamlit as st
from PIL import Image
import io
import zipfile

def render():
    st.title("🖼️ 画像一括リサイズ")
    st.write("複数の画像を選択し、指定した方法で一括リサイズします。")

    uploaded_files = st.file_uploader("画像を選択（複数可）", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    resize_mode = st.selectbox("リサイズ方法を選択", [
        "縮小率（%）",
        "高さ（px）",
        "幅（px）",
        "長辺（px）",
        "短辺（px）"
    ])

    # 入力UI
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

    if uploaded_files:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file in uploaded_files:
                img = Image.open(file)
                aspect_ratio = img.width / img.height

                # リサイズ処理（比率維持）
                if resize_mode == "縮小率（%）":
                    new_size = (
                        int(img.width * scale_percent / 100),
                        int(img.height * scale_percent / 100)
                    )
                elif resize_mode == "高さ（px）":
                    new_size = (
                        int(target_height * aspect_ratio),
                        target_height
                    )
                elif resize_mode == "幅（px）":
                    new_size = (
                        target_width,
                        int(target_width / aspect_ratio)
                    )
                elif resize_mode == "長辺（px）":
                    if img.width >= img.height:
                        new_size = (
                            target_long,
                            int(target_long / aspect_ratio)
                        )
                    else:
                        new_size = (
                            int(target_long * aspect_ratio),
                            target_long
                        )
                elif resize_mode == "短辺（px）":
                    if img.width <= img.height:
                        new_size = (
                            target_short,
                            int(target_short / aspect_ratio)
                        )
                    else:
                        new_size = (
                            int(target_short * aspect_ratio),
                            target_short
                        )

                resized_img = img.resize(new_size, Image.LANCZOS)

                # 表示
                st.image(resized_img, caption=f"{file.name}（{resize_mode}でリサイズ）", use_column_width=False)
                st.write(f"元サイズ: {img.width} × {img.height} → 新サイズ: {resized_img.width} × {resized_img.height}")

                # 個別ダウンロード
                buf = io.BytesIO()
                resized_img.save(buf, format="PNG")
                st.download_button(
                    label=f"{file.name} を保存",
                    data=buf.getvalue(),
                    file_name=f"resized_{file.name}",
                    mime="image/png"
                )

                # ZIPに追加
                zip_file.writestr(f"resized_{file.name}", buf.getvalue())

        # ZIP一括ダウンロード
        st.download_button(
            label="📦 一括ダウンロード（ZIP）",
            data=zip_buffer.getvalue(),
            file_name="resized_images.zip",
            mime="application/zip"
        )

# 実行
if __name__ == "__main__":
    render()

