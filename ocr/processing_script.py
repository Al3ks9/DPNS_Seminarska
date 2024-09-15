import Levenshtein
import pandas as pd
import cv2
import numpy as np

source_folder = './images/'
df = pd.read_csv('new__out.csv', encoding_errors='ignore', na_values=None, keep_default_na=False)
id_df = df.groupby('id')
document_source = './dokumenti_dpns/'


def levenshtein_accuracy(ocr_text, actual_text):
    distance = Levenshtein.distance(ocr_text.lower(), actual_text.lower())
    max_length = max(len(actual_text), len(ocr_text))
    accuracy = (max_length - distance) / max_length
    return accuracy


def preprocess_image(image_id):
    path = source_folder + image_id + '.jpg'
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(thresh, kernel, iterations=1)
    eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
    return eroded_image

def preprocess_image_2(image_id):
    path = source_folder + image_id + '.jpg'

    # Load the image
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adaptive histogram equalization (CLAHE) for localized contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(gray)

    # Apply mild denoising focused on preserving edges
    denoised_image = cv2.fastNlMeansDenoising(contrast_enhanced, None, h=15, templateWindowSize=7, searchWindowSize=21)

    # Apply sharpening to enhance text edges while preserving clarity
    kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened_image = cv2.filter2D(denoised_image, -1, kernel_sharpening)

    # Final touch: slight GaussianBlur to smooth the edges
    final_image = cv2.GaussianBlur(sharpened_image, (1, 1), 0)

    return final_image

def preprocess_image_3(image_id):
    path = source_folder + image_id + '.jpg'

    # Load the image
    img = cv2.imread(path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply light contrast enhancement
    contrast_enhanced = cv2.convertScaleAbs(gray, alpha=1.2, beta=20)

    # Apply very mild denoising
    denoised_image = cv2.fastNlMeansDenoising(contrast_enhanced, None, h=10)

    # Apply sharpening to make text edges sharper
    kernel_sharpening = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(denoised_image, -1, kernel_sharpening)

    return sharpened_image


# def preprocess_document(image_id):
#     path = document_source + image_id + '.png'
#     img = cv2.imread(path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
#
#     kernel = np.ones((3, 3), np.uint8)
#     dilated_image = cv2.dilate(thresh, kernel, iterations=1)
#     eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
#     return eroded_image


import cv2
import numpy as np


def preprocess_document(image_id):
    path = document_source + image_id + '.png'

    # Load the image
    img = cv2.imread(path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE to improve contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    # Apply adaptive thresholding
    adaptive_thresh = cv2.adaptiveThreshold(
        enhanced_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Optional: Apply morphological transformation to clean the image
    kernel = np.ones((2, 2), np.uint8)  # Kernel size for morphological operations
    cleaned_image = cv2.medianBlur(adaptive_thresh, 3)  # Apply median blur to reduce noise

    cv2.imwrite('./output_dokumenti' + image_id + '.png', cleaned_image)
    return cleaned_image


def process_true_text(image_id):
    filtered_rows = id_df.get_group(image_id)
    text = list(filtered_rows['text'])
    text.sort()
    spaced_list = [line.split(' ') for line in text]
    new_list = [el for line in spaced_list for el in line]
    new_list.sort()
    return ''.join(new_list)


def process_tesseract_text(string):
    if string == '':
        return ''
    text_list = string.split('\n')
    text_list.sort()
    spaced_list = [line.split(' ') for line in text_list if line != '']
    new_list = [el for line in spaced_list for el in line]
    new_list.sort()
    return ''.join(new_list)


def process_easyocr_text(results):
    res = pd.DataFrame(results, columns=['bbox', 'text', 'conf'])
    text_list = res['text'].values.tolist()
    text_list.sort()
    spaced_list = [line.split(' ') for line in text_list if line != '']
    new_list = [el for line in spaced_list for el in line]
    new_list.sort()
    return ''.join(new_list)


def compare_accuracy(image_id, original_output, processed_output):
    true_text = process_true_text(image_id)
    original_acc = levenshtein_accuracy(original_output, true_text)
    processed_acc = levenshtein_accuracy(processed_output, true_text)
    if original_acc > processed_acc:
        return 1, original_acc
    else:
        return 0, processed_acc
