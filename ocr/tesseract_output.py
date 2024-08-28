import pytesseract
from new_ids import ids
from PIL import Image
from processing_script import process_tesseract_text


if __name__ == '__main__':
    text_output = open('text_output_tesseract.txt', 'w')
    i = 0
    for ID in ids:
        img = Image.open('./images/' + '008cfef3402609bf' + '.jpg')
        text = pytesseract.image_to_string(img, lang='eng')
        text_output.write(process_tesseract_text(text))
        text_output.write('\n\n')
        print(i)
        i += 1
    text_output.close()
