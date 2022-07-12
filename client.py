import os
import tkinter as gui
from pdf2image import convert_from_path as pdf
from ImageCutter import *

leftFirstImageCropPercentage  = (0.1006, 0.2086, 0.4983, 0.9068)
rightFirstImageCropPercentage = (0.5147, 0.2086, 0.9125, 0.9068)

leftImageCropPercentage  = (0.1006, 0.1250, 0.4983, 0.9068)
rightImageCropPercentage = (0.5147, 0.1250, 0.9125, 0.9068)

srcList = filedialog.askopenfilenames(title = "Select PDF files to cut", filetypes = [("PDF Files", ".pdf")])

for src in srcList:

    pageNum = 1
    pdfFile = pdf(src, dpi = 600)
    fileName, fileExt = os.path.splitext(src)

    for pdfImage in pdfFile:
        pdfImage.save(f"{fileName}-PAGE#{pageNum}-L.png")
        pdfImage.save(f"{fileName}-PAGE#{pageNum}-R.png")

        if pageNum % 4 == 1:
            leftCropRange  = leftFirstImageCropPercentage
            rightCropRange = rightFirstImageCropPercentage
        else:
            leftCropRange  = leftImageCropPercentage
            rightCropRange = rightImageCropPercentage
        
        imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-L.png", cropRange = leftCropRange, cropCheckRange = (0.0420, 0.120))
        imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-R.png", cropRange = rightCropRange, cropCheckRange = (0.0420, 0.120))

        os.remove(f"{fileName}-PAGE#{pageNum}-L.png")
        os.remove(f"{fileName}-PAGE#{pageNum}-R.png")
        pageNum += 1