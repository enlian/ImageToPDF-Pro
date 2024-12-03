import os
import subprocess
import concurrent.futures
from tqdm import tqdm
from datetime import datetime
from PIL import Image

# 增加 Pillow 的图像像素限制
Image.MAX_IMAGE_PIXELS = None

# 设置路径
input_dir = 'output_20241203_181629'
output_dir = f'output_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
executable_path = './ai/realesrgan-ncnn-vulkan.exe'

# 创建输出文件夹
os.makedirs(output_dir, exist_ok=True)

def process_image(file_name):
    input_path = os.path.join(input_dir, file_name)
    output_path = os.path.join(output_dir, file_name)

    try:
        # 调用命令行工具
        result = subprocess.run([executable_path, '-i', input_path, '-o', output_path, '-s', '4'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result.check_returncode()

        if not os.path.exists(output_path):
            raise FileNotFoundError(f"输出文件 {output_path} 未生成。")

    except Exception as e:
        print(f"处理 {file_name} 时发生错误: {e}")

def main():
    # 获取文件列表
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # 使用进度条和线程池执行多线程处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        list(tqdm(executor.map(process_image, files), total=len(files), desc="Processing Images"))

if __name__ == '__main__':
    main()
