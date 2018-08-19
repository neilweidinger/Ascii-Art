from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from search import binarySearch, leftmost, rightmost

# returns 2D array of rgb data [0, 0] corresponding to top left corner of image
def extractRGBdata(image):
    data = list(image.getdata())
    width, height = image.size

    rgbVals = []

    count = 0
    row = []
    for r, g, b in data:
        row.append((r, g, b))
        count += 1

        if count % width == 0:
            rgbVals.append(row)
            row = []

    return rgbVals

def printRGBvals(rgbVals):
    for row in rgbVals:
        for pixel in row:
            print("{}\t".format(pixel), end="")
        print("")

def getUnoptimizedCharDict(font):
    charDict= {}

    for i in range(32, 127):
        charImage = Image.new('RGB', (70, 90), (255, 255, 255)) # new blank image
        draw = ImageDraw.Draw(charImage) # create ImageDraw object
        draw.text((0, 0), chr(i), fill=(0, 0, 0), font=font) # draw char onto image

        charDict[getBrightnessAverage(extractRGBdata(charImage))] = chr(i) # brightnessAvg:char

    return charDict

# returns average brightness of a specified patch of pixels
def getBrightnessAverage(rgbData):
    width = len(rgbData[0])
    height = len(rgbData)

    bTotal = 0
    for row in rgbData:
        for rgbPixel in row:
            bTotal += (sum(rgbPixel) / 3)
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
    font = ImageFont.truetype("Fonts/Courier.ttf", 100)
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
    pixelPatchLen = 10

    for r in range(0, rgbHeight, pixelPatchLen):

        rowContainingAvgBrightness = []

        for c in range(0, rgbWidth, pixelPatchLen):
            pixelPatch = []

            for patchRow in range(r, min(r + pixelPatchLen, rgbHeight)):
                pixelPatchRow = []

                for patchCol in range(c, min(c + pixelPatchLen, rgbWidth)):
                    pixelPatchRow.append(rgbData[patchRow][patchCol])

                pixelPatch.append(pixelPatchRow)

            patchAvgBrightness = int(getBrightnessAverage(pixelPatch))
            print(getBrightnessToChar(patchAvgBrightness, weightings, keys), end=" ")
            rowContainingAvgBrightness.append(patchAvgBrightness)

        print("")
        # print(rowContainingAvgBrightness)

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
    charWeightingsKeys = getCharWeightingsKeys(charWeightings)

    img = Image.open("Photos/Mona.png")
    contraster = ImageEnhance.Contrast(img)
    img = contraster.enhance(2.75)
    mapRGBtoChars(extractRGBdata(img), charWeightings, charWeightingsKeys)

    # charList = []
    # for comb in charWeightings.items():
        # charList.append(comb)
# 
    # charList.sort()
    # for comb in charList:
        # # print(comb[1], end=" ")
        # print(comb)
