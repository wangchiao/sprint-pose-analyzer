
import cv2
import mediapipe as mp
import numpy as np
from analyzer.pose_analyzer import calculate_angle
from analyzer.drawing_utils import draw_angle_text


def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, 30, (w, h))

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(model_complexity=1)
    mp_drawing = mp.solutions.drawing_utils

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            lm = results.pose_landmarks.landmark

            def get_point(idx):
                pt = lm[idx]
                return np.array([pt.x * w, pt.y * h])

            try:
                l_hip = get_point(mp_pose.PoseLandmark.LEFT_HIP.value)
                l_knee = get_point(mp_pose.PoseLandmark.LEFT_KNEE.value)
                l_ankle = get_point(mp_pose.PoseLandmark.LEFT_ANKLE.value)
                r_hip = get_point(mp_pose.PoseLandmark.RIGHT_HIP.value)
                r_knee = get_point(mp_pose.PoseLandmark.RIGHT_KNEE.value)
                r_ankle = get_point(mp_pose.PoseLandmark.RIGHT_ANKLE.value)
                l_foot = get_point(mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value)
                r_foot = get_point(mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value)
                l_shoulder = get_point(mp_pose.PoseLandmark.LEFT_SHOULDER.value)
                r_shoulder = get_point(mp_pose.PoseLandmark.RIGHT_SHOULDER.value)
                l_elbow = get_point(mp_pose.PoseLandmark.LEFT_ELBOW.value)
                r_elbow = get_point(mp_pose.PoseLandmark.RIGHT_ELBOW.value)

                draw_angle_text(frame, "l_knee", l_knee, calculate_angle(l_hip, l_knee, l_ankle), (-30, -10))
                draw_angle_text(frame, "r_knee", r_knee, calculate_angle(r_hip, r_knee, r_ankle), (20, -10))
                draw_angle_text(frame, "l_ankle", l_ankle, calculate_angle(l_knee, l_ankle, l_foot), (-30, 20))
                draw_angle_text(frame, "r_ankle", r_ankle, calculate_angle(r_knee, r_ankle, r_foot), (20, 20))
                draw_angle_text(frame, "l_shoulder", l_shoulder, calculate_angle(l_elbow, l_shoulder, l_hip), (-40, -20))
                draw_angle_text(frame, "r_shoulder", r_shoulder, calculate_angle(r_elbow, r_shoulder, r_hip), (30, -20))

                pelvis_center = ((l_hip + r_hip) / 2).astype(int)
                pelvis_y = (l_hip[1] + r_hip[1]) / 2
                draw_angle_text(frame, "pelvis_height", pelvis_center, pelvis_y, (0, 10))

            except:
                pass

        out.write(frame)

    cap.release()
    out.release()
    return output_path
