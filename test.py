import subprocess
import os

# —— 配置部分 —— #
video_path = r"D:\应用软件\Vscode\工作区\Image_edit\pn3.mp4"
output_gif_path = r"D:\应用软件\Vscode\工作区\Image_edit\pn4.gif"

# 背景抠图颜色（白色）
bg_color = "0xffffff"  # FFmpeg 十六进制颜色
tolerance = 0.1        # 容差，可调 0.0 ~ 1.0，抠图范围大，可能误抠；小，残影多
blend = 0.0            # 控制边缘平滑程度，混合度

# 压缩参数
fps = 10               # 帧率，流畅度，越低文件越小8~20
max_colors = 256       # 最大调色板颜色数64~256

# —— 检测 ffmpeg —— #
def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return 'ffmpeg'
    except FileNotFoundError:
        ffmpeg_path = input("未找到系统 ffmpeg，请输入 ffmpeg.exe 完整路径: ").strip('"')
        if os.path.isfile(ffmpeg_path):
            return ffmpeg_path
        else:
            raise FileNotFoundError("FFmpeg 路径无效！")

ffmpeg_cmd = check_ffmpeg()

# —— 生成 GIF 命令 —— #
# 使用调色板优化，先生成调色板再生成 GIF
cmd = [
    ffmpeg_cmd,
    '-i', video_path,
    '-vf',
    f"fps={fps},scale=iw:-1:flags=lanczos,colorkey={bg_color}:{tolerance}:{blend},"
    f"split[s0][s1];[s0]palettegen=max_colors={max_colors}[p];[s1][p]paletteuse",
    output_gif_path
]

# —— 执行命令 —— #
print("正在生成透明 GIF...")
subprocess.run(cmd)
print("GIF 已生成:", output_gif_path)