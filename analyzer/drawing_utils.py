import cv2

def angle_color(angle):
    if angle < 60:
        return (0, 0, 255)    # 紅
    elif angle < 120:
        return (0, 255, 255)  # 黃
    else:
        return (0, 255, 0)    # 綠

def draw_angle_text(frame, pos, angle, offset=(0, -15)):
    x, y = int(pos[0]) + offset[0], int(pos[1]) + offset[1]
    cv2.putText(frame, f"{int(angle)}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, angle_color(angle), 2)
