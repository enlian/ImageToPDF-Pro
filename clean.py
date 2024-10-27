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

# 设置 DPI 和增强参数
dpi = 600  # 可以根据需要调整 DPI
sharpness_factor = 1.5  # 锐化倍数

# 定义图像增强函数
def enhance_image(image):
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 应用直方图均衡化来提升对比度
    equalized = cv2.equalizeHist(gray)

    # 锐化处理 - 防止锐化过度
    blurred = cv2.GaussianBlur(equalized, (5, 5), 0)
    sharpened = cv2.addWeighted(equalized, 1.5, blurred, -0.5, 0)

    # 检查锐化后是否仍有有效内容
    if np.mean(sharpened) < 250:  # 避免锐化导致图像完全变白
        enhanced_image = sharpened
    else:
        enhanced_image = equalized  # 如果锐化导致图像变白，保持原图

    # 转换回 BGR 模式
    enhanced_image = cv2.cvtColor(enhanced_image, cv2.COLOR_GRAY2BGR)
    return enhanced_image

# 定义每个进程处理的函数
def process_page(page_data):
    page, index = page_data
    img = np.array(page)  # 将 PDF 页面转换为 NumPy 数组

    # 增强图像清晰度
    enhanced_img = enhance_image(img)

    # 将增强后的图像转换为 PIL Image 对象
    enhanced_pil_img = Image.fromarray(enhanced_img)

    # 清理未使用的图像对象，释放内存
    del img
    del enhanced_img
    gc.collect()  # 调用垃圾回收

    return enhanced_pil_img, index

# 处理PDF并行化，逐页处理
def process_pdf_in_parallel(pdf_path, dpi, start_page, end_page, timeout=600):
    results = []
    for page_num in tqdm(range(start_page, end_page + 1), desc="Processing pages"):
        try:
            # 每次只转换一页，并增加超时
            pages = convert_from_path(pdf_path, dpi=dpi, first_page=page_num, last_page=page_num, timeout=timeout)

            # 并行处理每一页，限制为 4 个并行进程
            with Pool(processes=4) as pool:
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

    # 并行处理 PDF 转换并增强
    processed_images = process_pdf_in_parallel(pdf_path, dpi, start_page, end_page)

    # 保存所有增强后的图像为一个 PDF
    output_pdf_path = os.path.join(output_dir, 'enhanced_output_combined.pdf')
    save_to_pdf(processed_images, output_pdf_path)

    print(f"所有增强后的图片和合成的PDF已经保存到 {output_dir} 文件夹中。")

# 运行主程序
if __name__ == '__main__':
    main()
