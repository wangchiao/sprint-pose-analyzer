import cv2
import mediapipe as mp
import numpy as np

class PoseAnalyzer:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(model_complexity=1)

    def calculate_angle(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        ba = a - b
        bc = c - b
        cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

    def process_frame(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        if not results.pose_landmarks:
            return None, {}

        h, w = frame.shape[:2]
        lm = results.pose_landmarks.landmark

        def get(index):
            pt = lm[index]
            return np.array([pt.x * w, pt.y * h])

        try:
            angles = {}

            # 下肢
            angles["l_knee"] = self.calculate_angle(get(23), get(25), get(27))
            angles["r_knee"] = self.calculate_angle(get(24), get(26), get(28))
            angles["l_ankle"] = self.calculate_angle(get(25), get(27), get(31))
            angles["r_ankle"] = self.calculate_angle(get(26), get(28), get(32))

            # 骨盆高度
            l_hip = get(23)
            r_hip = get(24)
            pelvis_center_y = (l_hip[1] + r_hip[1]) / 2
            angles["pelvis_height"] = pelvis_center_y

            # 肩膀與手肘
            angles["l_shoulder"] = self.calculate_angle(get(13), get(11), get(23))
            angles["r_shoulder"] = self.calculate_angle(get(14), get(12), get(24))


            return results.pose_landmarks, angles
        except:
            return results.pose_landmarks, {}
