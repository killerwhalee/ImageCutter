import os
from pdf2image import convert_from_path as pdf
from PIL import Image

def run(srcList, cropMode = "standard_type_A"):
    success, fail = (0, 0)

    # Load cropMode from cropData JSON file
    with open("json/cropData.json", "r") as cropJson:
        cropData = json.load(cropJson)
        leftFirstImageCropPercentage = cropData[cropMode]["leftFirstImageCropPercentage"]
        rightFirstImageCropPercentage = cropData[cropMode]["rightFirstImageCropPercentage"]

        leftImageCropPercentage = cropData[cropMode]["leftImageCropPercentage"]
        rightImageCropPercentage = cropData[cropMode]["rightImageCropPercentage"]

        cropCheckRange = cropData[cropMode]["cropCheckRange"]

    # Iterate for every source path in source list
    for src in srcList:
        print(f"Cutting [{src}]")

        '''
        if os.path.isdir(src):
            s, f = run(os.listdir(src))
            success, fail = success + s, fail + f
        '''

        # Catch every error/exception occur while running function
        try:
            pageNum = 1
            startNum = 1
            pdfFile = pdf(src, dpi = 600)
            fileName, fileExt = os.path.splitext(src)

            for pdfImage in pdfFile:
                pdfImage.save(f"{fileName}-PAGE#{pageNum}-L.png")
                pdfImage.save(f"{fileName}-PAGE#{pageNum}-R.png")
                #pageNum += 1; continue # For raw extraction

                # Typically first page has different form (case specific).
                # If not, FirstImageCropPercentage would be same with ImageCropPercentage in JSON file
                if pageNum % 4 == 1:
                    leftCropRange  = leftFirstImageCropPercentage
                    rightCropRange = rightFirstImageCropPercentage
                else:
                    leftCropRange  = leftImageCropPercentage
                    rightCropRange = rightImageCropPercentage
                
                # This is for Binary Cropping
                startNum += imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-L.png", dest = fileName, cropRange = leftCropRange, cropCheckRange = cropCheckRange, startNum = startNum, numDigit = 2)
                startNum += imgBinaryCrop(f"{fileName}-PAGE#{pageNum}-R.png", dest = fileName, cropRange = rightCropRange, cropCheckRange = cropCheckRange, startNum = startNum, numDigit = 2)

                # This is for Raw Cropping
                #startNum += imgRawCrop(f"{fileName}-PAGE#{pageNum}-L.png", dest = f"{fileName}-halfcrop", cropRange = leftCropRange, startNum = startNum, numDigit = 2)
                #startNum += imgRawCrop(f"{fileName}-PAGE#{pageNum}-R.png", dest = f"{fileName}-halfcrop", cropRange = rightCropRange, startNum = startNum, numDigit = 2)

                # Remove temporal file created
                os.remove(f"{fileName}-PAGE#{pageNum}-L.png")
                os.remove(f"{fileName}-PAGE#{pageNum}-R.png")

                pageNum += 1
            
            print(f"Successfully cut source [{src}]")
            success += 1

        # We caught some error/exception here.
        # Print error message and exit
        except Exception as e:
            print(f"Error in source [{src}] - {e}")
            fail += 1
    
    # Print result message then return with success/fail count
    print(f"Process Done: Success {success} / Fail {fail}")
    return success, fail
    
def imgBottomTrim(image, whiteSpace):
    #Image Bottom Trimming
    bottomLine = 0
    width, height = image.size
    
    for heightPixel in range(height):
        for widthPixel in range(int(width * 0.5)):
            if image.getpixel((widthPixel, heightPixel)) != (255, 255, 255):
                bottomLine = heightPixel
                break

    recroppedRegion = 0, 0, width, min(bottomLine + 2 * whiteSpace, height)
    image = image.crop(recroppedRegion)
    return image

def imgRawCrop(src, dest = None, cropRange = (0, 0, 1, 1), startNum = 1, numDigit = 0):
    if not dest:
        dest = os.path.splitext(src)[0]
    else:
        dest = os.path.splitext(dest)[0]

    image = Image.open(src)
    width, height = image.size
    imageCount = 0
    
    ## Crop Image
    imageCropArea = (int(cropRange[0] * width), int(cropRange[1] * height), int(cropRange[2] * width), int(cropRange[3] * height))
    croppedImage = image.crop(imageCropArea)

    imageStr = str(startNum + imageCount)
    if numDigit:
        imageStr = "0" * (numDigit - len(str(startNum + imageCount))) + str(startNum + imageCount)

    croppedImage.save(f"{dest}_{imageStr}.png")

    return 1


def imgBinaryCrop(src, dest = None, cropRange = (0, 0, 1, 1), cropCheckRange = (0, 0), startNum = 1, numDigit = 0):

    if not dest:
        dest = os.path.splitext(src)[0]
    else:
        dest = os.path.splitext(dest)[0]

    image = Image.open(src)
    width, height = image.size
    
    ## Crop Image
    imageCropArea = (int(cropRange[0] * width), int(cropRange[1] * height), int(cropRange[2] * width), int(cropRange[3] * height))
    croppedImage = image.crop(imageCropArea)
    width, height = croppedImage.size
    whiteSpace = int(height * 0.005)

    ## Variable Set
    imageCount = 0
    boundRange  = [0, 0]
        
    #Cut Each Paragraph in Cropped Page
    for heightPixel in range(height):
        for widthPixel in range(int(width * cropCheckRange[1])):
            if croppedImage.getpixel((widthPixel, heightPixel)) != (255, 255, 255):
                if widthPixel < width * cropCheckRange[0]:
                    if boundRange[1]:
                        recroppedRegion = 0, max(boundRange[0] - whiteSpace, 0), width, heightPixel - whiteSpace
                        croppedHeight = (heightPixel - 1) - max(boundRange[0] - whiteSpace, 0)

                        if boundRange[0]:
                            imageStr = str(startNum + imageCount)
                            if numDigit:
                                imageStr = "0" * (numDigit - len(str(startNum + imageCount))) + str(startNum + imageCount)

                            unTrimmedImage = croppedImage.crop(recroppedRegion)
                            outputImage = imgBottomTrim(unTrimmedImage, whiteSpace)
                            outputImage.save(f"{dest}_{imageStr}.png")

                            imageCount += 1
                        
                        boundRange = [0, 0]
                    
                    if not boundRange[0]:
                        boundRange[0] = heightPixel
                    
                else:
                    boundRange[1] = heightPixel
                
                break

    recroppedRegion = 0, max(boundRange[0] - whiteSpace, 0), width, heightPixel - whiteSpace
    croppedHeight = (heightPixel - 1) - max(boundRange[0] - whiteSpace, 0)
    
    
    if boundRange[0]:
        imageStr = str(startNum + imageCount)
        imageStr = "0" * (numDigit - len(str(startNum + imageCount))) + str(startNum + imageCount)

        unTrimmedImage = croppedImage.crop(recroppedRegion)
        outputImage = imgBottomTrim(unTrimmedImage, whiteSpace)
        outputImage.save(f"{dest}_{imageStr}.png")

        imageCount += 1

    return imageCount
