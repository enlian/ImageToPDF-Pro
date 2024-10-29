import os
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
from tqdm import tqdm
from datetime import datetime
from multiprocessing import Pool
import gc

# PDF 文件路径
pdf_path = '1.pdf'

# 设置 DPI 和裁剪参数
dpi = 600  # 更新为 600 DPI

# 单独设置左右和上下的裁剪比例
extra_crop_left_percentage = 0.07   # 左边裁剪
extra_crop_right_percentage = 0.07  # 右边裁剪
extra_crop_top_percentage = 0.06     # 上边裁剪
extra_crop_bottom_percentage = 0.07  # 下边裁剪

# 原始裁剪参数（相对于原始 900 DPI）
original_crop_x_start = int(1695 * dpi / 900)
original_crop_y_start = int(900 * dpi / 900)
original_crop_width = int(2931 * dpi / 900)
original_crop_height = int(4453 * dpi / 900)

# 根据裁剪比例调整左右和上下的裁剪范围
crop_x_start = original_crop_x_start + int(original_crop_width * extra_crop_left_percentage)  # 左边裁剪
crop_y_start = original_crop_y_start + int(original_crop_height * extra_crop_top_percentage)   # 上边裁剪
crop_width = original_crop_width - int(original_crop_width * (extra_crop_left_percentage + extra_crop_right_percentage))  # 总宽度减少左右的裁剪
crop_height = original_crop_height - int(original_crop_height * (extra_crop_top_percentage + extra_crop_bottom_percentage))  # 总高度减少上下的裁剪

# 定义每个进程处理的函数
def process_page(page_data):
    page, index, output_dir = page_data
    img = np.array(page)  # 将 PDF 页面转换为 NumPy 数组
    height, width = img.shape[:2]

    # 确保裁剪范围不超过图像边界
    crop_x_end = min(crop_x_start + crop_width, width)
    crop_y_end = min(crop_y_start + crop_height, height)

    # 裁剪图像
    img_cropped = img[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

    # 将裁剪后的图像转换为 PIL Image 对象
    cropped_img = Image.fromarray(img_cropped)

    # 保存裁剪后的图像为 PNG
    image_path = os.path.join(output_dir, f"page_{index}.png")
    cropped_img.save(image_path, "PNG")

    # 清理未使用的图像对象，释放内存
    del img
    del img_cropped
    gc.collect()  # 调用垃圾回收

    return image_path

# 处理PDF并行化，逐页处理，避免超时问题
def process_pdf_in_parallel(pdf_path, dpi, start_page, end_page, output_dir, timeout=600):
    for page_num in tqdm(range(start_page, end_page + 1), desc="Processing pages"):
        try:
            # 每次只转换一页，并增加超时
            pages = convert_from_path(pdf_path, dpi=dpi, first_page=page_num, last_page=page_num, timeout=timeout)

            # 使用并行处理限制进程数
            with Pool(processes=6) as pool:  # 限制为 4 个进程并行
                pool.map(process_page, [(pages[0], page_num, output_dir)])

        except Exception as e:
            print(f"Error processing page {page_num}: {e}")
            continue

# 主程序
def main():
    # 创建输出文件夹
    output_dir = f'processed_output_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 指定要处理的页面范围
    start_page = 19
    end_page = 393  # 根据 PDF 页数调整

    # 并行处理 PDF 转换并裁剪
    process_pdf_in_parallel(pdf_path, dpi, start_page, end_page, output_dir)

    print(f"所有图片已保存到 {output_dir} 文件夹中。")

# 运行主程序
if __name__ == '__main__':
    main()
