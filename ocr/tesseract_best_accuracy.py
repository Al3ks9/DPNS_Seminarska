import pytesseract
from new_ids import ids
from processing_script import *

if __name__ == '__main__':
    source_folder = './images/'
    output_folder = './output_images/'
    overall_accuracy = 0
    i = 0
    for image_id in ids:
        print(i)
        i += 1
        original = cv2.imread(source_folder + image_id + '.jpg')
        processed = preprocess_image(image_id)
        true_text = process_true_text(image_id)
        output_text_original = pytesseract.image_to_string(original)
        output_text_processed = pytesseract.image_to_string(processed)
        original_text = process_tesseract_text(output_text_original)
        processed_text = process_tesseract_text(output_text_processed)
        result = compare_accuracy(image_id, original_text, processed_text)

        if result[0]:
            cv2.imwrite(output_folder + image_id + '.jpg', original)
        else:
            cv2.imwrite(output_folder + image_id + '.jpg', processed)

        overall_accuracy += result[1]

    print(overall_accuracy / 423)
