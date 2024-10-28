
from time import sleep
import os
import shutil

from pdfminer.high_level import extract_text
from pdfminer.pdfpage import PDFPage
from PyPDF2 import PdfReader
from transformers import pipeline
import cv2
 
doc = "../DataSheetElec.pdf"
reader = PdfReader(doc)
VARIANCE_THRESHOLD = 100.0
 
def is_notBlurry (filename):
    image = cv2.imread(filename, 0)
    variance = cv2.Laplacian(image,cv2.CV_64F).var()
    return variance >= VARIANCE_THRESHOLD
#--------------------------- init output text and foler -------------------------------#

if not os.path.exists("outputImages"):
    os.makedirs("outputImages")
else:
    shutil.rmtree("outputImages")
    os.makedirs("outputImages")

with open("outputExtract.txt ", 'w') as f:
    f.write("")
 
#--------------------- Extraction du texte en utilisant pdfminer -----------------------#
 
with open(doc, 'rb') as f:
    # Parcourir chaque page
    for page_num, page in enumerate(PDFPage.get_pages(f), start=1):
        # Extraire le texte de la page courante
        print("extraction texte page ", page_num)
        page_text = extract_text(f, page_numbers=[page_num-1])
        with open("outputExtract.txt", "a", encoding="utf-8") as fichier:
            fichier.write(page_text)
 
        pageImg = reader.pages[page_num-1]
        print("extraction of the images in page ", page_num)
        count = 0

        #Check if page foler exists
        imgDirec = "outputImages/page"+str(page_num)
        if not os.path.exists(imgDirec):
            os.makedirs(imgDirec)


        for image_file_object in pageImg.images:
            with open( imgDirec + "/"  +str(count)+ image_file_object.name, "wb") as fp:
                fp.write(image_file_object.data)
                count += 1
 
        captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        print("checking if there are images worth adding")
        for filename in os.listdir(imgDirec):
            image_path = os.path.join(imgDirec,filename)
            if is_notBlurry(image_path):
                desc = "il y a une image : "+captioner("outputPyPDF2/"+filename)[0]["generated_text"]+"\n"
                with open("outputExtract.txt", "a", encoding="utf-8") as fichier:
                    fichier.write(desc)
        print("parsing of page ", str(page_num), " complete")
 
print("parsing complete in outputExtract.txt")