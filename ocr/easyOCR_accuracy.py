import os
import keras_ocr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytesseract
from PIL import Image
from easyocr import Reader


def easyocr_annotate(img_fn, ez_results, ts_results):
    fig, axs = plt.subplots(1, 2, figsize=(18, 10))

    easy_df = pd.DataFrame(ez_results, columns=['bbox', 'text', 'conf'])
    easy_results = easy_df[['text', 'bbox']].values.tolist()
    easy_results = [(x[0], np.array(x[1])) for x in easy_results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn), easy_results, ax=axs[0])

    tess_df = pd.DataFrame(ts_results, columns=['bbox', 'text', 'conf'])
    tess_results = tess_df[['text', 'bbox']].values.tolist()
    tess_results = [(x[0], np.array(x[1])) for x in tess_results]
    keras_ocr.tools.drawAnnotations(plt.imread(img_fn), tess_results, ax=axs[1])

    plt.savefig('./compare_images/' + image_fn, bbox_inches='tight', pad_inches=0)
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
            # if int(tesseract_data['conf'][i]) > 0:
            text = tesseract_data['text'][i]
            conf = float(tesseract_data['conf'][i])
            x, y, w, h = tesseract_data['left'][i], tesseract_data['top'][i], tesseract_data['width'][i], \
                tesseract_data['height'][i]
            bbox = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
            tesseract_results.append((bbox, text, conf))

        easyocr_annotate(source_folder + image_fn, easy_results, tesseract_results)
