# -*- encoding: utf-8 -*-

import pymupdf # imports the library
import pytesseract
from PIL import Image
import io


def extract_text_with_ocr(pdf_path):
    """
    Extracts text from a PDF, using OCR for image-only pages.
    """
    all_text = ""
    with pymupdf.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)

            # First, try standard text extraction
            text = page.get_text("text")
            if text.strip():
                all_text += text + "\n"
                continue  # Move to the next page if text is found

            # If no text, assume it's a scanned page and use OCR
            print(f"Performing OCR on page {page_num + 1}...")

            # Render the page to a high-resolution pixmap (image)
            pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))  # Use a zoom factor for better resolution
            img_bytes = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_bytes))

            # Use Tesseract to perform OCR on the image
            ocr_text = pytesseract.image_to_string(image)
            all_text += ocr_text + "\n"

    return all_text

pdf_file = './JOGOS_REALIZADOS.pdf'

extracted_content = extract_text_with_ocr(pdf_file)
print(extracted_content)

# Optional: Save the extracted text to a file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(extracted_content)