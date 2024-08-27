import pandas as pd
from easyocr import Reader
import os
from new_ids import ids

if __name__ == '__main__':
    source_folder = './images/'
    # text_output = open('text_output_easyocr1.txt', 'w')
    text_output = open('text_output_easyocr_all.txt', 'w')

    # ids = ['0002c799b0cd7412', '0002cb8d8ea5eb7e', '0002f9c7fac5f093', '000a1a700c0c7950',
    #        '000aecd78b230135', '000bd0b4fa27644c', '000ca4a1855318b1', '000ed967c71e566f',
    #        '00c359f294f7dcd9', '01aa9b9a3520fc0c']

    reader = Reader(['en'])
    image_files = [img + '.jpg' for img in ids]
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
