import cv2

# 视频路径
video_path = r"D:\应用软件\Vscode\工作区\Image_edit\pn2.mp4"
output_path = r"D:\应用软件\Vscode\工作区\Image_edit\pn2_cropped_batch.mp4"

# 打开视频
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 视频写入器
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# 鼠标回调函数，用来获取裁剪矩形
refPt = []
cropping = False
exit_program = False
crop_selected = False

def click_and_crop(event, x, y, flags, param):
    global refPt, cropping, crop_selected
    if crop_selected:
        return
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        cv2.rectangle(frame_display, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("Frame", frame_display)

# 读取第一帧
ret, frame = cap.read()
if not ret:
    print("无法读取视频")
    cap.release()
    out.release()
    exit()

frame_display = frame.copy()
clone = frame.copy()
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_and_crop)

print("请在第一帧用鼠标框选裁剪区域，然后按 'c' 确认, 'r' 重置, 'ESC' 退出")
while True:
    cv2.imshow("Frame", frame_display)
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        exit_program = True
        break
    elif key == ord("r"):
        frame_display = clone.copy()
        refPt = []
    elif key == ord("c"):
        if len(refPt) == 2:
            x1, y1 = refPt[0]
            x2, y2 = refPt[1]
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            crop_selected = True
            break
        else:
            print("请先用鼠标框选裁剪区域")

cv2.destroyAllWindows()

if not crop_selected or exit_program:
    print("未选择裁剪区域或用户退出，程序终止")
    cap.release()
    out.release()
    exit()

# 裁剪第一帧并写入
cropped = frame[y1:y2, x1:x2]
cropped = cv2.resize(cropped, (width, height))
out.write(cropped)

# 批量裁剪剩余帧
for i in range(1, frame_count):
    ret, frame = cap.read()
    if not ret:
        break
    cropped = frame[y1:y2, x1:x2]
    cropped = cv2.resize(cropped, (width, height))
    out.write(cropped)

cap.release()
out.release()
print("批量裁剪完成，视频保存到:", output_path)