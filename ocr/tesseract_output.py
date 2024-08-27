import pytesseract
from new_ids import ids
from PIL import Image


def process_string(string):
    if string == '':
        return ''
    text_list = string.split('\n')
    text_list.sort()
    spaced_list = [line.split(' ') for line in text_list if line != '']
    new_list = [el for line in spaced_list for el in line]
    new_list.sort()
    return new_list


if __name__ == '__main__':
    text_output = open('text_output_tesseract.txt', 'w')
    i = 0
    for ID in ids:
        img = Image.open('./images/' + ID + '.jpg')
        text = pytesseract.image_to_string(img, lang='eng')
        text_output.write('\n'.join(process_string(text)))
        text_output.write('\n\n')
        print(i)
        i += 1
    text_output.close()
