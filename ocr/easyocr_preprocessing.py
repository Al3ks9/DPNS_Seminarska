from new_ids import ids
from easyocr import Reader
from processing_script import *
import cv2

if __name__ == '__main__':
    source_folder = './images/'
    output_folder = './easy_ ocr_pre_2/'
    overall_accuracy = 0
    i = 0
    reader = Reader(['en'])
    for image_id in ids:
        i += 1
        print(i)
        original = cv2.imread(source_folder + image_id + '.jpg')
        processed = preprocess_image_2(image_id)
        results_processed = reader.readtext(processed)
        processed_text = process_easyocr_text(results_processed)
        true_text = process_true_text(image_id)
        accuracy = levenshtein_accuracy(processed_text, true_text)

        cv2.imwrite(output_folder + image_id + '.jpg', processed)

        overall_accuracy += accuracy

    print(overall_accuracy / 423)