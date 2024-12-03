import os
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
from tqdm import tqdm
from datetime import datetime
from multiprocessing import Pool, cpu_count
import gc

# 可修改参数
pdf_path = '1.pdf'  # PDF 文件路径
start_page = 1  # 要处理的起始页
end_page = 279  # 要处理的结束页
dpi = 300  # 转换时的 DPI
target_width = 1200  # 目标宽度分辨率，防止变形

# 定义每个进程处理的函数
def process_page(page_data):
    page, index, output_dir = page_data
    img = np.array(page)  # 将 PDF 页面转换为 NumPy 数组

    # 将图像转换为 PIL Image 对象
    full_img = Image.fromarray(img)

    # 计算新高度以保持宽高比
    width, height = full_img.size
    aspect_ratio = height / width
    target_height = int(target_width * aspect_ratio)

    # 调整图像大小
    full_img = full_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

    # 保存图像为 PNG
    image_path = os.path.join(output_dir, f"page_{index}.png")
    full_img.save(image_path, "PNG")

    # 清理未使用的图像对象，释放内存
    del img
    gc.collect()  # 调用垃圾回收

    return image_path

# 处理PDF并行化，逐页处理
def process_pdf_in_parallel(pdf_path, dpi, start_page, end_page, output_dir, timeout=1200):
    with Pool(processes=max(1, cpu_count() // 2)) as pool:
        for page_num in tqdm(range(start_page, end_page + 1), desc="Processing pages"):
            try:
                # 转换单页 PDF
                pages = convert_from_path(pdf_path, dpi=dpi, first_page=page_num, last_page=page_num, timeout=timeout)

                # 分页保存为图像
                pool.map(process_page, [(pages[0], page_num, output_dir)])
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
                continue

# 主程序
def main():
    # 创建输出文件夹
    output_dir = f'output_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 并行处理 PDF 转换
    process_pdf_in_parallel(pdf_path, dpi, start_page, end_page, output_dir)

    print(f"所有图片已保存到 {output_dir} 文件夹中。")

# 运行主程序
if __name__ == '__main__':
    main()
