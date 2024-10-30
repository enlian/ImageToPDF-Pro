import os
from PIL import Image
from tqdm import tqdm
from datetime import datetime
import gc
import re

# 输入文件夹路径和输出 PDF 文件路径
input_folder = 'super'  # 替换为你的图片文件夹路径
output_pdf = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

# 使用正则表达式从文件名中提取数字，并按数字顺序排序
def sort_key(filename):
    match = re.search(r'page_(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

# 获取文件夹中的所有图片文件并排序
image_files = sorted(
    [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))],
    key=sort_key
)

# 定义一个生成器，逐页加载和保存图片，以降低内存使用
def generate_images(skip_first=False):
    for i, filename in enumerate(tqdm(image_files, desc="Converting Images to PDF")):
        if skip_first and i == 0:
            continue  # 跳过第一个文件
        input_path = os.path.join(input_folder, filename)
        try:
            with Image.open(input_path) as img:
                img = img.convert("RGB")  # 转换为 RGB 模式
                img.info['dpi'] = (600, 600)  # 设置 DPI 为 600
                yield img
                gc.collect()  # 手动回收内存
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

# 将生成的图片逐页保存为 PDF
first_image = next(generate_images(), None)
if first_image:
    # 使用第一个图片生成 PDF，跳过重复第一页
    first_image.save(output_pdf, save_all=True, append_images=list(generate_images(skip_first=True)), quality=85, optimize=True)
    print(f"PDF 已保存到: {output_pdf}")
else:
    print("没有可用的图片来生成 PDF 文件。")

# 清理内存
del first_image
gc.collect()
