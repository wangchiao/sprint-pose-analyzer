import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

offsets = {
    "l_knee": (-20, -10),
    "r_knee": (20, -10),
    "l_ankle": (-20, 10),
    "r_ankle": (20, 10),
    "pelvis_height": (-20, -20),
    "l_shoulder": (-40, -20),
    "r_shoulder": (40, -20),
}

def angle_color_gradient(angle):
    # 紅 → 黃 → 綠（小角度紅，大角度綠）
    angle = max(0, min(180, angle))

    if angle <= 90:
        # 紅（255,0,0）→ 黃（0,255,255）
        b = 0
        g = int((angle / 90) * 255)
        r = 255
    else:
        # 黃（0,255,255）→ 綠（0,255,0）
        b = 0
        g = 255
        r = int(255 - ((angle - 90) / 90) * 255)

    return (b, g, r)  # OpenCV 使用 BGR 格式

def draw_landmarks_with_angles(frame, landmarks, angles):
    if landmarks:
        h, w = frame.shape[:2]
        lm = landmarks.landmark

        mp_drawing.draw_landmarks(
            frame,
            landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)
        )

        def get_px(index):
            pt = lm[index]
            return int(pt.x * w), int(pt.y * h)

        positions = {
            "l_knee": get_px(mp_pose.PoseLandmark.LEFT_KNEE.value),
            "r_knee": get_px(mp_pose.PoseLandmark.RIGHT_KNEE.value),
            "l_ankle": get_px(mp_pose.PoseLandmark.LEFT_ANKLE.value),
            "r_ankle": get_px(mp_pose.PoseLandmark.RIGHT_ANKLE.value),
            "pelvis_height": get_px(mp_pose.PoseLandmark.LEFT_HIP.value),
            "l_shoulder": get_px(mp_pose.PoseLandmark.LEFT_SHOULDER.value),
            "r_shoulder": get_px(mp_pose.PoseLandmark.RIGHT_SHOULDER.value),
         
        }

        for label, value in angles.items():
            if label in positions:
                x, y = positions[label]
                dx, dy = offsets.get(label, (0, 0))
                cv2.putText(frame, f"{int(value)}", (x + dx, y + dy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, angle_color_gradient(value), 2)

    return frame
