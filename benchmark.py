from PyPDF2 import PdfReader
from time import sleep

#-------------------------PyPDF-------------------------------------------------------#
"""
L'extraction d'images de PyPDF est la meilleure, les images gardent leur transparence
Pour l'extraction de texte, dans le cas particulier que c'est une diapositive, 
le texte est extrait dans un ordre illogique pour la comprehension du texte,
Il commence par le header et le footer, puis a fait le tour des blocs colorés,
sans ordre.
"""
with open("outputPyPDF2/outputPyPDF2.txt", "w", encoding="utf-8") as fichier:
            fichier.write("")

reader = PdfReader("document.pdf")
pagenb = 1
for page in reader.pages:
    text = page.extract_text()
    count = 0
    for image_file_object in page.images:
        with open("outputPyPDF2/"+str(count)+ image_file_object.name, "wb") as fp:
            fp.write(image_file_object.data)
            count += 1
    pagenb+=1
    with open("outputPyPDF2/outputPyPDF2.txt", "a", encoding="utf-8") as fichier:
        fichier.write(text)
    
#-------------------------PyMuPDF-------------------------------------------------------#
"""
J'ai pu extraire les images avec cette bibliotèque aussi, mais il y a pas mal de carrés noirs,
transparence perdue dans l'extraction.
Pour l'extraction du texte, cela commencait bien, avec une approche colonne par colonne,
mais au milieu d'un paragraphe, la bib m'a sorti un titre qui se situe de l'autre coté du document.
"""
import pymupdf  # PyMuPDF
import io
from PIL import Image

with open("outputPyMuPDF/outputPyMuPDF.txt", "w", encoding="utf-8") as fichier:
            fichier.write("")

# Ouvrir le fichier PDF
pdf_path = "document.pdf"
document = pymupdf.open(pdf_path)
page_num = 0
for page in document:
    page_num += 1
    blocks = page.get_text("blocks") 
    images = page.get_images(full=True)

    for image_index, img in enumerate(images):
        xref = img[0]
        base_image = document.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]

        image_name = f"image_page{page_num}_{image_index+1}.{image_ext}"
        image_path = "outputPyMuPDF/"+image_name
        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)

    # Trier les blocs de texte selon la position (Y puis X)
    sorted_blocks = sorted(blocks, key=lambda b: (b[0], b[1]))  # Trier par Y, puis par X

    # Afficher les blocs de texte dans l'ordre des positions
    for block in sorted_blocks:
        x0, y0, x1, y1, text,_,oui2 = block  # Coordonnées et texte du bloc
        print(f"Position: ({x0}, {y0}) - ({x1}, {y1})")
        print(f"Texte: {text}\n")

        with open("outputPyMuPDF/outputPyMuPDF.txt", "a", encoding="utf-8") as fichier:
            fichier.write(text)

# Fermer le document PDF
document.close()

#--------------------------pdfplumber-----------------------------------------------------#
"""
pdf plumber suis une approche de gauche a droite, mais n'a pas bien decouppé les blocs
donc plutot que de revenir a la ligne pour finir un paragraphe, mon code a continue la ligne
pour lire un autre bloc
"""
import pdfplumber

with open("outputpdfplumber.txt", "w", encoding="utf-8") as fichier:
            fichier.write("")

with pdfplumber.open('document.pdf') as pdf:
    pages = pdf.pages
    for page in pages:
        text = page.extract_text()

        with open("outputpdfplumber.txt", "a", encoding="utf-8") as fichier:
            fichier.write(text)

#---------------------------pdfMiner--------------------------------------------------#
"""
pdf miner a l'ai d'etre le plus efficace pour l'extraction de texte:
c'est une approche par colonne de haut en bas.
Tout les blocs ont bien etes decoupes, le seul probleme serait 
que la lecture a un peu deconne au niveau des listes 

▪ Nomenclature Générale des Actes 

▪

Professionnels pour les consultations 
et visites – NGAP
Classification Commune des Actes 
Médicaux pour les actes techniques - 
CCAM

plutot que : 

▪ Nomenclature Générale des Actes 
Professionnels pour les consultations 
et visites – NGAP
▪Classification Commune des Actes 
Médicaux pour les actes techniques - 
CCAM
"""
from pdfminer.high_level import extract_text


# Extraire le texte du PDF
texte = extract_text("document.pdf")


# Optionnel : sauvegarder le texte dans un fichier
with open("outputpdfMiner.txt", "w", encoding="utf-8") as fichier:
    fichier.write(texte)