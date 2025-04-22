import streamlit as st
import tempfile
import os
from analyzer.video_processor import process_video

st.set_page_config(page_title="Sprint Pose Analyzer", layout="centered")
st.title("🏃‍♂️ Sprint Pose Analyzer")
st.write("上傳影片，標註骨架後自動輸出")

uploaded_file = st.file_uploader("請上傳影片（mp4/mov/avi）", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name
        output_path = input_path.replace(".mp4", "_output.mp4")

    with st.spinner("影片處理中..."):
        result_path = process_video(input_path, output_path)

    st.success("✅ 分析完成")
    st.video(result_path)

    with open(result_path, "rb") as f:
        st.download_button("📥 下載分析影片", f, file_name="analyzed_video.mp4", mime="video/mp4")
