from pdfminer.high_level import extract_text
from pdfminer.pdfpage import PDFPage
from PyPDF2 import PdfReader
from time import sleep
import os
from transformers import pipeline

doc = "document.pdf"
#----- Extraction du texte en utilisant pdfminer ---------------------------------------#
print("extraction of the text in ", doc)
texte = extract_text(doc)


with open("outputpdfMiner.txt", "w", encoding="utf-8") as fichier:
    fichier.write(texte)

print("extraction complete in outputpdfMiner.txt")
#--------------Extraction des images avec pyPDF2 ---------------------------------------#
print("extraction of the images in ", doc)

reader = PdfReader(doc)
pagenb = 1
for page in reader.pages:
    count = 0
    for image_file_object in page.images:
        with open("outputPyPDF2/"+str(count)+ image_file_object.name, "wb") as fp:
            fp.write(image_file_object.data)
            count += 1
    pagenb+=1

print("image extraction complete in outputPyPDF2 folder")

#---------------------Analyse des images ----------------------------------------------#
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
for filename in os.listdir("outputPyPDF2"):
    captioner("outputPyPDF2/"+filename)
