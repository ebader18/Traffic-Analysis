import cv2
import ctypes

# Set windows size based on display's resolution
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
print("Screen resolution:", screen_width, "x", screen_height)
window_size = (int(screen_height / 1.25), int(screen_width / 1.25))


def navigate_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Reached the end or failed to read the video")
            break
        
        factor = min(window_size[0] / frame.shape[0], window_size[1] / frame.shape[1])
        frame = cv2.resize(frame, (0, 0), interpolation=cv2.INTER_NEAREST, fx=factor, fy=factor)
        cv2.rectangle(frame, (0, 0), (250, 50), (255, 255, 255), thickness=-1)
        cv2.putText(frame, f'Image #{current_frame}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 0), 2)
        cv2.imshow('Video Navigation', frame)

        key = cv2.waitKey(0) & 0xFF
        if key == ord('d'):
            if current_frame < total_frames - 1:
                current_frame += 1
            else:
                current_frame = 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
                
        elif key == ord('a'):
            if current_frame > 0:
                current_frame -= 1
            else:
                current_frame = total_frames - 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        elif key == ord('s'):
            cv2.imwrite(f'img_{current_frame:04}.png', frame)
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path = 'video_002.webm'
    navigate_video(video_path)
