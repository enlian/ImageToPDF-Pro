import os
from PIL import Image
from tqdm import tqdm
from datetime import datetime
import gc
import re
from PyPDF2 import PdfMerger

# Input folder and output PDF path
input_folder = 'output_20241203_182059'  # Replace with your image folder path
final_output_pdf = f"final_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
temp_folder = "temp_pdfs"

# Create temporary folder
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# Sort files based on numbers in their filenames
def sort_key(filename):
    match = re.search(r'page_(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

# Get sorted list of image files
image_files = sorted(
    [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))],
    key=sort_key
)

# Chunk size for processing
chunk_size = 50
temp_pdfs = []

for i in range(0, len(image_files), chunk_size):
    chunk_files = image_files[i:i + chunk_size]
    output_pdf = os.path.join(temp_folder, f"temp_chunk_{i//chunk_size + 1}.pdf")
    temp_pdfs.append(output_pdf)

    try:
        # Load images in one pass and add progress bar
        images = []
        for filename in tqdm(chunk_files, desc=f"Processing chunk {i//chunk_size + 1}/{len(image_files)//chunk_size + 1}"):
            input_path = os.path.join(input_folder, filename)
            try:
                with Image.open(input_path) as img:
                    img = img.convert("RGB")
                    img.info['dpi'] = (600, 600)  # Set DPI
                    images.append(img.copy())  # Copy image to avoid closing issues
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

        # Save chunk as a temporary PDF
        if images:
            images[0].save(output_pdf, save_all=True, append_images=images[1:], quality=85, optimize=True)
            print(f"Saved chunk to: {output_pdf}")
        else:
            print(f"No images found for chunk: {output_pdf}")
    except Exception as e:
        print(f"Error saving chunk {i//chunk_size + 1}: {e}")
    finally:
        gc.collect()  # Manually release memory

# Merge all temporary PDFs into the final PDF
merger = PdfMerger()
for pdf in temp_pdfs:
    merger.append(pdf)

merger.write(final_output_pdf)
merger.close()

# Clean up temporary files
for temp_pdf in temp_pdfs:
    os.remove(temp_pdf)
os.rmdir(temp_folder)

print(f"Final PDF file has been created: {final_output_pdf}")
