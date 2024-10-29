import os
import subprocess
import threading
import concurrent.futures
from tqdm import tqdm
from PIL import Image
from datetime import datetime

# 设置路径
input_dir = 'imgs600dpi'
output_dir = f'processed_output_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
executable_path = './ai/realesrgan-ncnn-vulkan.exe'

# 创建输出文件夹
os.makedirs(output_dir, exist_ok=True)

def process_image(file_name):
    """
    处理单个图像文件，将其传递给 realesrgan-ncnn-vulkan.exe 进行高清化处理。
    """
    input_path = os.path.join(input_dir, file_name)
    output_path = os.path.join(output_dir, file_name)
    
    try:
        # 调用命令行工具
        result = subprocess.run([executable_path, '-i', input_path, '-o', output_path,'-s','4'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result.check_returncode()  # 如果返回码不是0，则引发异常

    except subprocess.CalledProcessError as e:
        print(f"处理 {file_name} 时发生错误: {e}")
    
    finally:
        # 释放图像资源
        Image.open(input_path).close()
        Image.open(output_path).close()

def main():
    # 获取文件列表
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # 使用进度条和线程池执行多线程处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        list(tqdm(executor.map(process_image, files), total=len(files), desc="Processing Images"))

if __name__ == '__main__':
    main()
