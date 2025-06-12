from PIL import Image
import pytesseract

# Load image and run OCR
image = Image.open("C:\\Users\\Acer\\Downloads\\ChatGPT Image May 3, 2025, 01_11_31 PM.png")
text = pytesseract.image_to_string(image)

print("Extracted Text:")
print(text)
