"""
Code to transform a pdf into png image
"""
import fitz 
file_path = "steval-stwinwfv1.pdf"
doc = fitz.open(file_path)  # open document
for i, page in enumerate(doc):
    pix = page.get_pixmap()  # render page to an image
    pix.save(f"outImg/page_{i}.png")