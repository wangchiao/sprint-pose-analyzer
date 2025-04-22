
import streamlit as st
import tempfile
import os
from analyzer.video_processor import process_video_with_plot
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sprint Pose Analyzer", layout="centered")
st.title("🏃‍♂️ Sprint Pose Analyzer")
st.write("上傳短跑影片，系統會分析並標註關節角度與骨架 ✨")

uploaded_file = st.file_uploader("請上傳影片檔（支援 mp4、mov、avi、mkv）", type=["mp4", "mov", "avi", "mkv"])

os.makedirs("output", exist_ok=True)

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name
        output_path = os.path.join("output", os.path.basename(input_path).replace(".mp4", "_output.mp4"))

        with st.spinner("🚀 正在分析影片，請稍候..."):
            angle_df = process_video_with_plot(input_path, output_path)

        st.success("✅ 分析完成！以下是結果：")
        st.video(output_path)

        with open(output_path, "rb") as file:
            st.download_button("📥 下載分析影片", file, file_name="analyzed_sprint.mp4", mime="video/mp4")

        if angle_df is not None and not angle_df.empty:
            st.subheader("📈 每一幀關節角度變化圖")
            joints = angle_df.columns.tolist()
            for joint in joints:
                st.line_chart(angle_df[joint], height=200, use_container_width=True)
