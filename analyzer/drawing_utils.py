
import cv2

def angle_color(angle):
    if angle < 60:
        return (0, 0, 255)
    elif angle < 120:
        return (0, 255, 255)
    else:
        return (0, 255, 0)

def draw_angle_text(frame, label, pos, angle, offset=(0, 0)):
    x, y = int(pos[0]) + offset[0], int(pos[1]) + offset[1]
    color = angle_color(angle)
    cv2.putText(frame, f"{int(angle)}", (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
