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

# 单独设置左右和上下的裁剪比例
extra_crop_left_percentage = 0.07   # 左边裁剪
extra_crop_right_percentage = 0.07  # 右边裁剪
extra_crop_top_percentage = 0.06     # 上边裁剪
extra_crop_bottom_percentage = 0.07  # 下边裁剪

# 原始裁剪参数
original_crop_x_start = 1695
original_crop_y_start = 900
original_crop_width = 2931
original_crop_height = 4453

# 根据裁剪比例调整左右和上下的裁剪范围
crop_x_start = original_crop_x_start + int(original_crop_width * extra_crop_left_percentage)  # 左边裁剪 extra_crop_left_percentage
crop_y_start = original_crop_y_start + int(original_crop_height * extra_crop_top_percentage)   # 上边裁剪 extra_crop_top_percentage
crop_width = original_crop_width - int(original_crop_width * (extra_crop_left_percentage + extra_crop_right_percentage))  # 总宽度减少左右的裁剪
crop_height = original_crop_height - int(original_crop_height * (extra_crop_top_percentage + extra_crop_bottom_percentage))  # 总高度减少上下的裁剪

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
            with Pool(processes=4) as pool:  # 限制为 6 个进程并行
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
    if not images:  # 检查是否有处理成功的图片
        print("No images were processed. PDF will not be created.")
        return

    # 获取所有处理完的图像，并根据它们的顺序合成为一个 PDF
    images_sorted = sorted(images, key=lambda x: x[1])
    pil_images = [img[0] for img in images_sorted]

    if pil_images:  # 如果有图片，则保存为 PDF
        pil_images[0].save(output_pdf_path, save_all=True, append_images=pil_images[1:])
    else:
        print("No images to save.")

# 主程序
def main():
    # 创建输出文件夹
    output_dir = f'processed_output_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    start_page = 19
    end_page = 393  # 根据 PDF 页数调整    end_page = 393


    # 并行处理 PDF 转换并裁剪
    processed_images = process_pdf_in_parallel(pdf_path, dpi, start_page, end_page)

    # 保存所有裁剪后的图像为一个 PDF
    output_pdf_path = os.path.join(output_dir, 'output_combined.pdf')
    save_to_pdf(processed_images, output_pdf_path)

    print(f"所有图片和合成的PDF已经保存到 {output_dir} 文件夹中。")

# 运行主程序
if __name__ == '__main__':
    main()
