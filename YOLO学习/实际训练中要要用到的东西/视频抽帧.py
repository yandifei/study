import cv2
import os
from pathlib import Path

def extract_frames(video_path, output_dir, frame_interval=30):
    """
    从视频中抽取帧并保存为 (1).png, (2).png ...
    :param video_path: 视频文件路径
    :param output_dir: 输出目录（会自动创建）
    :param frame_interval: 每隔多少帧保存一帧（例如 30 表示每秒保存 1 帧，假设视频 30fps）
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频文件: {video_path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"视频总帧数: {total_frames}, FPS: {fps:.2f}")

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 每隔 interval 帧保存一次
        if frame_count % frame_interval == 0:
            saved_count += 1
            filename = f"({saved_count}).png"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
            print(f"已保存: {filepath}")

        frame_count += 1

    cap.release()
    print(f"抽帧完成，共保存 {saved_count} 张图片。")

"""需要创建的文件夹和要改的文件夹"""
video_path = r"抽帧出来的地方/2.mp4"  # 你的视频路径
output_dir = r"output"            # 输出文件夹


frame_interval = 30      # 每隔 30 帧抽一帧（如果视频是 30fps，则每秒抽一张）
extract_frames(video_path, output_dir, frame_interval)