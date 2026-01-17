import os
import shutil
import random

def split_yolo_dataset(src_path, dest_path, train_ratio=0.8):
    # 1. 定义路径
    src_images = os.path.join(src_path, 'images')
    src_labels = os.path.join(src_path, 'labels')
    classes_file = os.path.join(src_path, 'classes.txt')

    for split in ['train', 'val']:
        os.makedirs(os.path.join(dest_path, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(dest_path, split, 'labels'), exist_ok=True)

    # 2. 获取所有图片名 (不含后缀)
    image_files = [f for f in os.listdir(src_images) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_names = [os.path.splitext(f)[0] for f in image_files]

    # 3. 打乱并划分
    random.shuffle(image_names)
    split_idx = int(len(image_names) * train_ratio)
    train_names = image_names[:split_idx]
    val_names = image_names[split_idx:]

    def copy_files(names, split):
        for name in names:
            # 查找原图后缀
            img_ext = ""
            for ext in ['.jpg', '.jpeg', '.png']:
                if os.path.exists(os.path.join(src_images, name + ext)):
                    img_ext = ext
                    break

            if img_ext:
                # 移动图片
                shutil.copy2(os.path.join(src_images, name + img_ext),
                             os.path.join(dest_path, split, 'images', name + img_ext))
                # 移动标签
                label_path = os.path.join(src_labels, name + '.txt')
                if os.path.exists(label_path):
                    shutil.copy2(label_path, os.path.join(dest_path, split, 'labels', name + '.txt'))

    # 执行复制
    print(f"正在处理训练集 ({len(train_names)} 张)...")
    copy_files(train_names, 'train')
    print(f"正在处理验证集 ({len(val_names)} 张)...")
    copy_files(val_names, 'val')

    # 4. 自动生成 data.yaml
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines() if line.strip()]

    yaml_content = f"""
path: {os.path.abspath(dest_path)}
train: train/images
val: val/images

names:
"""
    for i, cls in enumerate(classes):
        yaml_content += f"  {i}: {cls}\n"

    with open(os.path.join(dest_path, 'data.yaml'), 'w') as f:
        f.write(yaml_content)

    print(f"\n✅ 完成！数据集已准备在: {dest_path}")
    print(f"🚀 你可以直接使用 {os.path.join(dest_path, 'data.yaml')} 进行训练了。")


# --- 使用设置 ---
if __name__ == "__main__":
    # 填入你从 Label Studio 解压后的文件夹路径
    source_folder = "./label_studio_export"
    # 填入你想生成的训练数据集存放路径
    output_folder = "./yolo_dataset"

    split_yolo_dataset(source_folder, output_folder, train_ratio=0.8)