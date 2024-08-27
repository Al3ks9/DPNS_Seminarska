import pandas as pd
from easyocr import Reader
import os

if __name__ == '__main__':
    source_folder = './images/'
    text_output = open('text_output_easyocr_all.txt', 'w')

    reader = Reader(['en'])
    image_files = [img for img in os.listdir(source_folder)]
    i = 0
    for image_fn in image_files:
        print(i)
        i += 1
        path = source_folder + image_fn
        results = reader.readtext(path)
        res = pd.DataFrame(results, columns=['bbox', 'text', 'conf'])
        text = res['text'].values.tolist()
        text.sort()
        text_output.write('\n'.join(text))
        text_output.write('\n')
        text_output.write('\n')
    text_output.close()
