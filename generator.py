from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from search import binarySearch, leftmost, rightmost
import os

# returns 2D array of rgb data [0, 0] corresponding to top left corner of image
def extractRGBdata(image):
    data = list(image.getdata())
    width, height = image.size

    rgbVals = []
    count = 0
    row = []

    for vals in data:
        row.append(vals[0:3])
        count += 1

        if count % width == 0: # we've finished one horizontal line of pixels, start new line
            rgbVals.append(row)
            row = []

    return rgbVals

def printRGBvals(rgbVals):
    for row in rgbVals:
        for pixel in row:
            print("{}\t".format(pixel), end="")
        print("")

def getUnoptimizedCharDict(font):
    charDict = {}

    for i in range(32, 127):
    # for i in list(range(32, 127)) + list(range(9617, 9620)) + list(range(9608, 9609)):
    # for i in list(range(32, 127)) + list(range(9617, 9620)):
        charImage = Image.new('RGB', (70, 90), (0, 0, 0)) # new blank image
        draw = ImageDraw.Draw(charImage) # create ImageDraw object
        draw.text((0, 0), chr(i), fill=(255, 255, 255), font=font) # draw char onto image

        bIndex = getBrightnessAverage(extractRGBdata(charImage))
        charDict[bIndex] = chr(i) # put our char into our dict using the format brightnessAvg:char

    return charDict

# returns average brightness of a specified patch of pixels (Doesn't have to be a whole image!)
def getBrightnessAverage(rgbData):
    width = len(rgbData[0])
    height = len(rgbData)

    bTotal = 0 # brightness total

    for row in rgbData:
        for rgbPixel in row:
            bTotal += (sum(rgbPixel) / 3) # add brightness of each pixel

    bAverage = bTotal / (width * height)
    return bAverage

# this function just adjusts our character weightings to a scale of [0, 255]
def getOptimizedCharDict(font):
    charDict = getUnoptimizedCharDict(font)
    newCharDict = {}

    min, max = getMinMaxKey(charDict)

    for bAverage, char in charDict.items():
        scaledB = int((255 * (bAverage - min)) / (max - min)) # truncate each key just to make things simpler
        newCharDict[scaledB] = char

    return newCharDict

def getMinMaxKey(charDict):
    keys = list(charDict.keys())
    min = 999
    max = -999
    for key in keys:
        if key < min:
            min = key
        if key > max:
            max = key

    return min, max

def getCharWeightings():
    font = ImageFont.truetype("Fonts/Menlo.ttc", 100)
    optimizedCharDict = getOptimizedCharDict(font)
    
    return optimizedCharDict

# returns a list of keys in our char weightings dictionary
def getCharWeightingsKeys(weightings):
    keyList = []
    for key in weightings.keys():
        keyList.append(key)

    keyList.sort()
    return keyList

def mapRGBtoChars(rgbData, weightings, keys):
    rgbWidth = len(rgbData[0])
    rgbHeight = len(rgbData)

    # here we make sure that our ascii art always fits within the width of our terminal
    terminalWidth = int(os.popen('tput cols', 'r').read()) # width is returned as str so convert to int

    if rgbWidth <= terminalWidth:
        pixelPatchLen = 1
    else:
        # ceil our number then * 2 to account for spaces taking up half our possible terminal area
        pixelPatchLen= int(rgbWidth / terminalWidth + 1) * 2

    for row in range(0, rgbHeight, pixelPatchLen):
        for col in range(0, rgbWidth, pixelPatchLen):
            pixelPatch = getPixelPatch(row, col, pixelPatchLen, rgbData, rgbHeight, rgbWidth)

            patchAvgBrightness = int(getBrightnessAverage(pixelPatch))
            print(getBrightnessToChar(patchAvgBrightness, weightings, keys), end=" ")

        print("")

def getPixelPatch(row, col, pixelPatchLen, rgbData, rgbHeight, rgbWidth):
    pixelPatch = []

    for patchRow in range(row, min(row + pixelPatchLen, rgbHeight)):
        pixelPatchRow = []

        for patchCol in range(col, min(col + pixelPatchLen, rgbWidth)):
            pixelPatchRow.append(rgbData[patchRow][patchCol])

        pixelPatch.append(pixelPatchRow)

    return pixelPatch

def getBrightnessToChar(bAverage, weightings, keyList):
    # warning: binarySearch only returns INDEX of closest brightness value, not brightness value itself
    keyIndex = binarySearch(keyList, bAverage)
    if keyIndex != -1:
        return weightings[keyList[keyIndex]]

    pred = leftmost(keyList, bAverage)
    succ = rightmost(keyList, bAverage)

    if bAverage - pred > succ - bAverage:
        return weightings[keyList[succ]]
    else:
        return weightings[keyList[pred]]

if __name__ == "__main__":
    charWeightings = getCharWeightings()
    charWeightings[0] = chr(32) # make sure space character is included in weightings
    charWeightingsKeys = getCharWeightingsKeys(charWeightings)

    img = Image.open("Photos/Mona.png")
    contraster = ImageEnhance.Contrast(img)
    img = contraster.enhance(2)
    mapRGBtoChars(extractRGBdata(img), charWeightings, charWeightingsKeys)

    # charList = []
    # for comb in charWeightings.items():
        # charList.append(comb)
# 
    # charList.sort()
    # for comb in charList:
        # # print(comb[1], end=" ")
        # print(comb)
