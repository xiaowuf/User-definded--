import cv2
import numpy as np
from PIL import Image

# 视频路径
video_path = r"D:\应用软件\Vscode\工作区\Image_edit\pn3.mp4"
# 输出 GIF 路径
output_gif_path = r"D:\应用软件\Vscode\工作区\Image_edit\pn4.gif"

# 读取视频
cap = cv2.VideoCapture(video_path)
frames = []

# 获取视频帧率
fps = cap.get(cv2.CAP_PROP_FPS)
frame_duration = int(1000 / fps)  # ms

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 转成 RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 创建 mask，检测白色背景
    # 白色阈值可调整，如果背景是纯白可用[245,245,245]~[255,255,255]
    lower = np.array([200, 200, 200], dtype=np.uint8)
    upper = np.array([255, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(frame_rgb, lower, upper)  # 白色区域 mask=255
    
    # 转成 RGBA
    frame_rgba = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2RGBA)
    
    # 将白色区域透明化
    frame_rgba[:, :, 3] = 255 - mask  # 白色部分 alpha=0
    
    # 转为 PIL 图像
    pil_img = Image.fromarray(frame_rgba)
    frames.append(pil_img)

cap.release()

if frames:
    # 保存为 GIF
    frames[0].save(
        output_gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=0,
        transparency=0,  # 确保透明通道
        disposal=2        # 每帧单独处理，防止堆叠残影
    )
    print("GIF 已生成:", output_gif_path)
else:
    print("未读取到视频帧，GIF未生成")