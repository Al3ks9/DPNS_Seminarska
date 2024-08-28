import os

import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
from new_ids import ids
from easyocr import Reader
import Levenshtein
import pytesseract
from tesseract_output import process_string


def levenshtein_accuracy(ocr_text, actual_text):
    distance = Levenshtein.distance(ocr_text.lower(), actual_text.lower())
    max_length = max(len(actual_text), len(ocr_text))
    accuracy = (max_length - distance) / max_length
    return accuracy


if __name__ == '__main__':
    source_folder = './images/'
    output_folder = './preprocessed_images/'

    true = "114:17/11/20092009-2010:7BBCCATEGORIESCHANNELSEastEnders:EpisodeEpisodeGear:HelpHomeHorizon:HowInsectsIt'sJamesLife:LongMOSTMay'sOnlyPOPULARPieceRadioSONYScalextricSearchSeriesSettingsStories:StringTVTheory:TopToyaaisiPlayerofBack"

    reader = Reader(['en'])
    for id in ids:
        img = source_folder + "008cfef3402609bf" + '.jpg'
        img = cv2.imread(img)
        cv2.imshow('original', img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        kernel = np.ones((3, 3), np.uint8)
        # Apply dilation
        dilated_image = cv2.dilate(thresh, kernel, iterations=1)
        eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
        data = reader.readtext(eroded_image)
        # print('processed')
        text = []
        for row in data:
            # print(row[1])
            text.append(row[1] + '\n')
        txt = ''.join(process_string(''.join(text)))
        data1 = reader.readtext(img)
        print('original')
        text1 = []
        for row in data1:
            # print(row[1])
            text1.append(row[1] + '\n')
        txt1 = ''.join(process_string(''.join(text1)))

        cv2.imshow('thresh', eroded_image)
        cv2.waitKey()

        # t1 = pytesseract.image_to_string(img)
        # t2 = pytesseract.image_to_string(eroded_image)

        # print(t1)
        # print(t2)
        #
        # txt = ''.join(process_string(t1))
        # txt1 = ''.join(process_string(t2))

        print(txt)
        print(txt1)

        print(levenshtein_accuracy(txt, true))
        print(levenshtein_accuracy(txt1, true))

        break
