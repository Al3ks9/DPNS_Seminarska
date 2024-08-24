from easyocr import Reader
import os

if __name__ == '__main__':
    source_folder = './images/'
    text_output = open('text_output_easyocr.txt', 'w')

    ids = [
        '000a1a700c0c7950',
        '000aecd78b230135',
        '000bd0b4fa27644c',
        '000ca4a1855318b1',
        '000ed967c71e566f',
        '0002c799b0cd7412',
        '0002cb8d8ea5eb7e',
        '0002f9c7fac5f093',
        '00c359f294f7dcd9',
        '01aa9b9a3520fc0c'
    ]

    reader = Reader(['en'])
    image_files = [img for img in os.listdir(source_folder)]
    for ID in ids:
        path = source_folder + ID + '.jpg'
        results = reader.readtext(path)
        text = results['text']
        text.sort()
        text_output.write(ID + '\n')
        text_output.write(text)
        text_output.write('\n')
        text_output.write('\n')
    text_output.close()
