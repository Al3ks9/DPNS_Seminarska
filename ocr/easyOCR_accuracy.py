import os
import keras_ocr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytesseract
from PIL import Image
from easyocr import Reader


def annotate_img(img_fn, res, choice):
    fig, axs = plt.subplots(1, 1, figsize=(15, 10))

    df = pd.DataFrame(res, columns=['bbox', 'text', 'conf'])
    results = df[['text', 'bbox']].values.tolist()
    results = [(x[0], np.array(x[1])) for x in results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn), results, ax=axs)

    plt.savefig('./compare_images_pairs/' + choice + image_fn, bbox_inches='tight', pad_inches=0)
    plt.close(fig)


if __name__ == '__main__':
    reader = Reader(['en'])
    source_folder = './images/'
    image_fns = [file for file in os.listdir('./images/')[:20]]

    for image_fn in image_fns:
        easy_results = reader.readtext(source_folder + image_fn)

        image = Image.open(source_folder + image_fn)
        tesseract_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

        tesseract_results = []
        for i in range(len(tesseract_data['text'])):
            text = tesseract_data['text'][i]
            conf = float(tesseract_data['conf'][i])
            x, y, w, h = tesseract_data['left'][i], tesseract_data['top'][i], tesseract_data['width'][i], \
                tesseract_data['height'][i]
            bbox = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
            tesseract_results.append((bbox, text, conf))

        annotate_img(source_folder + image_fn, easy_results, "easy_ocr_")
        annotate_img(source_folder + image_fn, tesseract_results, "tess_ocr_")
