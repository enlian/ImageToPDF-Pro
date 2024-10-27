# Enhance-Crop-PDF

Enhance-Crop-PDF is a Python-based tool designed to enhance and crop high-resolution PDF documents by converting them to images, performing specific cropping operations, and then converting the cropped images back into a consolidated PDF. This tool is particularly useful when dealing with large PDFs and documents where you need to enhance or crop specific sections.

## Features

- Converts high-resolution PDFs to images (with adjustable DPI).
- Allows precise cropping of specific areas based on pixel coordinates.
- Uses multiprocessing to process large PDFs efficiently.
- Automatically combines processed images back into a single PDF.

## Requirements

To use this project, you will need the following libraries and tools installed:

### Python Libraries

- **Python 3.6 or higher**
- **Pillow**: Python Imaging Library (PIL) fork for image processing.
- **pdf2image**: Converts PDF pages into images.
- **opencv-python**: OpenCV for image manipulation.
- **tqdm**: Progress bar utility for tracking the process.
- **multiprocessing**: Python’s built-in library for parallel processing.

You can install the necessary Python libraries by running:

```bash
pip install -r requirements.txt
```

### External Tools

- **Poppler**: A PDF rendering library. It is required for `pdf2image` to convert PDF pages into images.
  
  **Windows**:
  - Download and install Poppler for Windows from [here](https://blog.alivate.com.au/poppler-windows/).
  - After installing, add the path to the `bin` folder (e.g., `C:\path-to-poppler\bin`) to your system's environment `PATH`.

  **Linux**:
  ```bash
  sudo apt install poppler-utils
  ```

  **macOS**:
  ```bash
  brew install poppler
  ```

## Installation

1. Clone the repository or download the project files:

   ```bash
   git clone https://github.com/yourusername/Enhance-Crop-PDF.git
   cd Enhance-Crop-PDF
   ```

2. Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure that **Poppler** is installed and its path is properly configured in your system's `PATH` environment variable (see above).

## Usage

### Running the Tool

Once installed, you can run the tool using:

```bash
python app.py
```

By default, the tool will process the PDF named `1.pdf` in the current directory, converting it into high-resolution images, cropping the images, and merging them back into a PDF.

### Input PDF

Make sure your PDF file is placed in the same directory as the script or provide the full path in the script.

### Output

The processed images and the final combined PDF will be saved in a newly created directory named `processed_output_YYYYMMDD_HHMMSS`, where `YYYYMMDD_HHMMSS` is the current timestamp.

### Parameters

You can adjust the following parameters in the script to suit your needs:

1. **PDF File**:
   - Change the `pdf_path` variable to point to your desired PDF file:

     ```python
     pdf_path = 'your_pdf_file.pdf'
     ```

2. **DPI (Resolution)**:
   - The `dpi` setting controls the resolution of the output images. A higher DPI will result in clearer images but larger file sizes and more memory usage.
     
     Default:
     ```python
     dpi = 900
     ```
     
     You can adjust it to other values such as `300`, `600`, or `1200` depending on your needs.

3. **Cropping Parameters**:
   - The cropping is controlled by the `crop_x_start`, `crop_y_start`, `crop_width`, and `crop_height` variables. These parameters define the starting point and the size of the cropping area in pixels.
   
     Default cropping coordinates:
     ```python
     crop_x_start = 1695  # Start from 1695 pixels from the left
     crop_y_start = 900   # Start from 900 pixels from the top
     crop_width = 2931    # Width of the cropping area in pixels
     crop_height = 4453   # Height of the cropping area in pixels
     ```

     You can modify these values to define a different crop area, depending on the structure of your PDF.

4. **Parallel Processing**:
   - The tool uses parallel processing to handle large PDFs efficiently. You can modify the number of processes used by changing the `processes` parameter in the `Pool` constructor.
   
     Default:
     ```python
     with Pool(processes=4) as pool:  # Change 4 to your desired number of parallel processes
     ```

     Increase the number of processes if your system has enough memory and CPU cores, or decrease it if you're experiencing memory issues.

5. **Timeout**:
   - You can control the maximum time allowed for processing each page by adjusting the `timeout` parameter. The default is 600 seconds (10 minutes per page).
   
     Default:
     ```python
     timeout = 600  # 10 minutes timeout per page
     ```

6. **Page Range**:
   - You can adjust the `start_page` and `end_page` to limit the range of pages you want to process.
     
     Example:
     ```python
     start_page = 1
     end_page = 100  # Process only the first 100 pages
     ```

### Example

To run the script with a different PDF file (`sample.pdf`) and a lower DPI of 600, adjust the script as follows:

```python
pdf_path = 'sample.pdf'
dpi = 600
```

Then run:

```bash
python app.py
```

## Troubleshooting

### Poppler not found

If you see errors related to **Poppler** not being found, make sure that:
- Poppler is installed on your system.
- The path to Poppler’s `bin` directory is added to your system’s environment `PATH`.

### Memory Errors

If you encounter memory errors during processing:
- Reduce the number of parallel processes by adjusting `processes=4` to a lower number (e.g., `processes=2`).
- Lower the DPI setting to reduce the memory usage of each image.

### Timeout Errors

If some pages take too long to process, you may increase the `timeout` parameter or skip problematic pages by adjusting the page range.

## Contribution

Feel free to fork the project, submit issues, or create pull requests for any features or bug fixes.

## License

This project is licensed under the MIT License.