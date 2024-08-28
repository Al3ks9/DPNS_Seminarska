from new_ids import ids
from easyocr import Reader
from processing_script import *


if __name__ == '__main__':
    source_folder = './images/'
    output_folder = './output_images/'
    overall_accuracy = 0
    i = 0
    reader = Reader(['en'])
    for image_id in ids:
        print(i)
        i += 1
        original = cv2.imread(source_folder + image_id + '.jpg')
        processed = preprocess_image(image_id)
        results_original = reader.readtext(original)
        results_processed = reader.readtext(processed)
        original_text = process_easyocr_text(results_original)
        processed_text = process_easyocr_text(results_processed)
        result = compare_accuracy(image_id, original_text, processed_text)

        if result[0]:
            cv2.imwrite(output_folder + image_id + '.jpg', original)
        else:
            cv2.imwrite(output_folder + image_id + '.jpg', processed)

        overall_accuracy += result[1]

    print(overall_accuracy / 423)
