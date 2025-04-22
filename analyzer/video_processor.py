import cv2
from .pose_analyzer import PoseAnalyzer
from .drawing_utils import draw_landmarks_with_angles

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise Exception("❌ 無法開啟影片檔案")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    analyzer = PoseAnalyzer()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        landmarks, angles = analyzer.process_frame(frame)
        frame_with_info = draw_landmarks_with_angles(frame, landmarks, angles)
        out.write(frame_with_info)

    cap.release()
    out.release()

