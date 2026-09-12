import cv2
import os

def extract_frames(video_path, output_dir):
    """
    从视频中抽取帧并保存为 1.png, 2.png ...
    :param video_path: 视频文件路径
    :param output_dir: 输出目录（会自动创建）
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 打开视频
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频文件: {video_path}")
        return

    fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"视频总帧数: {total_frames}, 视频帧率: {fps} FPS, 分割图片数量：{int(total_frames / fps)}张")
    print(f"视频分辨率: {width}x{height}")


    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 每隔 interval 帧保存一次
        if frame_count % fps == 0:
            saved_count += 1
            filename = f"{saved_count}.png"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
            print(f"已保存: {filepath}")

        frame_count += 1

    cap.release()
    print(f"抽帧完成，共保存 {saved_count} 张图片。保存在: {output_dir}")

"""需要创建的文件夹和要改的文件夹"""
video_path = r"视频验证集/2.mp4"  # 你的视频路径
output_dir = r"images/val/2"            # 输出文件夹


extract_frames(video_path, output_dir)