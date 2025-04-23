import streamlit as st
import tempfile
from analyzer.video_processor import process_video

st.set_page_config(page_title="Sprint Pose Analyzer", layout="centered")
st.title("🏃‍♂️ Sprint Pose Analyzer")
st.write("上傳短跑影片，我們將分析並顯示骨架與關節角度")

uploaded_file = st.file_uploader("請上傳影片檔（支援 mp4、mov、avi、mkv）", type=["mp4", "mov", "avi", "mkv"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input:
        temp_input.write(uploaded_file.read())
        input_path = temp_input.name
        output_path = input_path.replace(".mp4", "_output.mp4")

    with st.spinner("分析中，請稍候..."):
        process_video(input_path, output_path)

    st.success("✅ 分析完成！以下是結果：")
    st.video(output_path)

    with open(output_path, "rb") as f:
        st.download_button("⬇️ 下載影片", f, file_name="analyzed_sprint.mp4", mime="video/mp4")
