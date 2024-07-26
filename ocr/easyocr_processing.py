from easyocr import Reader
import cv2
import os

if __name__ == '__main__':
    source_folder = './images/'
    output_folder = './output_images/'

    text_output = open('easyocr_text_outputs.txt', 'w')

    reader = Reader(['en'])
    image_files = [img for img in os.listdir(source_folder)]
    i = 0
    for image_file in image_files:
        print(i)
        i += 1
        path = source_folder + image_file
        image = cv2.imread(path)
        results = reader.readtext(image)
        image_id = os.path.basename(image_file)
        text_output.write(image_id + '\n')
        for result in results:
            bbox = result[0]
            top_left = tuple((int(i) for i in bbox[0]))
            bottom_right = tuple((int(i) for i in bbox[2]))
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 4)
            text_output.write(result[1] + '\n')
        text_output.write('\n')
        cv2.imwrite(output_folder + image_id, image)

