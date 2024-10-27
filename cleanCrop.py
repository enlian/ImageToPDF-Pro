import cv2
import os
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
from tqdm import tqdm
from datetime import datetime
from multiprocessing import Pool, cpu_count
import gc

# PDF 文件路径
pdf_path = '1.pdf'

# 设置 DPI 和裁剪参数
dpi = 900  # 高分辨率 DPI
crop_x_start = 1695  # 从左边距离 1695 像素开始裁剪
crop_y_start = 900   # 从顶部距离 900 像素开始裁剪
crop_width = 2931    # 裁剪宽度 2931 像素
crop_height = 4453   # 裁剪高度 4453 像素

# 定义每个进程处理的函数
def process_page(page_data):
    page, index = page_data
    img = np.array(page)  # 将 PDF 页面转换为 NumPy 数组
    height, width = img.shape[:2]

    # 确保裁剪范围不超过图像边界
    crop_x_end = min(crop_x_start + crop_width, width)
    crop_y_end = min(crop_y_start + crop_height, height)

    # 裁剪图像
    img_cropped = img[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

    # 将裁剪后的图像转换为 PIL Image 对象
    cropped_img = Image.fromarray(img_cropped)

    # 清理未使用的图像对象，释放内存
    del img
    del img_cropped
    gc.collect()  # 调用垃圾回收

    return cropped_img, index

# 处理PDF并行化，逐页处理，避免超时问题
def process_pdf_in_parallel(pdf_path, dpi, start_page, end_page, timeout=600):
    results = []
    for page_num in tqdm(range(start_page, end_page + 1), desc="Processing pages"):
        try:
            # 每次只转换一页，并增加超时
            pages = convert_from_path(pdf_path, dpi=dpi, first_page=page_num, last_page=page_num, timeout=timeout)

            # 限制并行处理进程数，根据系统配置建议 4-6 个进程
            with Pool(processes=4) as pool:  # 限制为 4 个进程并行
                result = pool.map(process_page, [(pages[0], page_num)])
                results.extend(result)

        except subprocess.TimeoutExpired:
            print(f"Timeout expired for page {page_num}. Skipping this page.")
            continue
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")
            continue

    return results

# 将结果保存为 PDF
def save_to_pdf(images, output_pdf_path):
    # 获取所有处理完的图像，并根据它们的顺序合成为一个 PDF
    images_sorted = sorted(images, key=lambda x: x[1])
    pil_images = [img[0] for img in images_sorted]

    # 将所有处理后的图像合成为 PDF
    pil_images[0].save(output_pdf_path, save_all=True, append_images=pil_images[1:])

# 主程序
def main():
    # 创建输出文件夹
    output_dir = f'processed_output_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start_page = 1
    end_page = 395  # 根据 PDF 页数调整

    # 并行处理 PDF 转换并裁剪
    processed_images = process_pdf_in_parallel(pdf_path, dpi, start_page, end_page)

    # 保存所有裁剪后的图像为一个 PDF
    output_pdf_path = os.path.join(output_dir, 'output_combined.pdf')
    save_to_pdf(processed_images, output_pdf_path)

    print(f"所有图片和合成的PDF已经保存到 {output_dir} 文件夹中。")

# 运行主程序
if __name__ == '__main__':
    main()
