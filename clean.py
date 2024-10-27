import subprocess

# PDF 文件路径
input_pdf = '1.pdf'
output_pdf = 'enhanced_output.pdf'

# 使用 --clean 和 --deskew 替代 --remove-background
subprocess.run(['ocrmypdf', '--clean', '--deskew', input_pdf, output_pdf])

print(f"Enhanced PDF saved to {output_pdf}")
