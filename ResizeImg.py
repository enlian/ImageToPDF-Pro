import os
from PIL import Image
from datetime import datetime
from tqdm import tqdm
import gc

# 输入和输出文件夹路径
input_folder = 'processed_output_20241030_004600'  # 替换为你的源文件夹路径
output_folder = datetime.now().strftime("output_images_%Y%m%d_%H%M%S")
os.makedirs(output_folder, exist_ok=True)  # 创建输出文件夹

# 缩小比例
resize_ratio = 0.4  # 缩小为原图的40%

# 获取文件夹中的所有图片文件
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))]

# 遍历并处理每张图片，带有进度条
for filename in tqdm(image_files, desc="Resizing Images"):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)
    
    try:
        # 打开并处理图片
        with Image.open(input_path) as img:
            # 计算缩小后的尺寸
            new_size = (int(img.width * resize_ratio), int(img.height * resize_ratio))
            img_resized = img.resize(new_size, Image.LANCZOS)

            # 保存到输出文件夹，转换 PNG 为 PNG8 格式
            if filename.lower().endswith('.png'):
                img_resized = img_resized.convert("P", palette=Image.ADAPTIVE, colors=256)
                img_resized.save(output_path, optimize=True, compress_level=0)  # PNG8 高品质压缩，低压缩级别
            elif filename.lower().endswith(('.jpg', '.jpeg')):
                img_resized.save(output_path, quality=100)  # 高质量 JPEG 压缩
            else:
                img_resized.save(output_path)  # 其他格式使用默认设置

            # 手动删除已处理对象并进行垃圾回收
            del img_resized
            gc.collect()

    except Exception as e:
        # 捕获并输出错误信息
        print(f"Error processing {filename}: {e}")
        continue

print(f"所有图片已缩小并保存到文件夹：{output_folder}")
