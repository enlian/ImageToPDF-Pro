## Image & PDF Toolkit

This project provides a set of scripts to process images and PDFs entirely on your local machine. All operations are done offline, ensuring your privacy. It’s designed to be quick and easy to use, especially for users who want efficient, local file processing.

### Installation

1. **Install Python Dependencies**: Ensure you have Python installed. Open a terminal or command prompt, navigate to the project folder, and run the following command to install the necessary dependencies:

   ```bash
   pip install pillow pymupdf tqdm
   ```

2. **Run a Script**: Depending on your needs, execute the relevant script. For example, to convert images to a PDF, use the command:

   ```bash
   python ImgsToPdf.py
   ```

3. **Check the Output**: After the script completes, the processed files will be saved in the specified output location, depending on the script. 

### Script Functions

Each script performs a unique function:

- **ClearImgsByAi.py**: Enhances image clarity using AI-based processing.
- **CropPdf.py**: Crops unwanted borders or sections from PDF files.
- **ImgsToPdf.py**: Converts a series of images into a single PDF file.
- **PdfToImgs.py**: Splits a PDF file into separate images, saving each page as an image.
- **ResizeImg.py**: Resizes images, allowing you to change resolution or dimensions.

### Customizing the Code (Example: Changing Input Folder)

Each script contains a variable for the input folder where files are read from. Here’s how you can modify it:

1. **Open the Script**: Open the script you want to modify (for example, `ImgsToPdf.py`) in a text editor.

2. **Find the Input Folder Path**: Look for a line of code near the top that defines `input_folder`, such as:

   ```python
   input_folder = 'highImgs'  # Original input folder path
   ```

3. **Change the Folder Path**: Replace `'highImgs'` with the path to your new folder. For example, if you want to use a folder named `images`, change it to:

   ```python
   input_folder = 'images'
   ```

4. **Save the Changes**: Save the modified script file.

5. **Run the Script Again**: Run the script as usual, and it will now use the updated folder path.

### Example Customization

Let’s say you want to change both the input and output folders for `ImgsToPdf.py`. Here’s what you would update:

```python
# Original code
input_folder = 'highImgs'
output_pdf = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

# Modified code
input_folder = 'my_images'  # New input folder path
output_pdf = 'outputs/my_pdf_output.pdf'  # New output path and filename
```

After making this change, the script will now read images from the `my_images` folder and save the PDF to `outputs/my_pdf_output.pdf`.

### Additional Notes

- **Make Sure the Folder Exists**: If the input or output folder does not exist, you may need to create it manually, or you can add code to create it automatically if needed.
- **Adjust Other Parameters**: You can also adjust parameters like DPI (image resolution) or quality settings in each script to control the output quality and file size.

### Security and Privacy

All processing is done locally, ensuring your files stay on your computer. This project is ideal for those who value privacy and want quick, local processing of image and PDF files.
