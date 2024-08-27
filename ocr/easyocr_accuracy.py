import Levenshtein


def levenshtein_accuracy(ocr_text, actual_text):
    distance = Levenshtein.distance(ocr_text.lower(), actual_text.lower())
    max_length = max(len(actual_text), len(ocr_text))
    if max_length == 0:
        return 1
    accuracy = (max_length - distance) / max_length
    return accuracy


def read_texts(lines):
    i = -1
    flag = True
    return_list = []
    while flag:
        text = ''
        i += 1
        if i >= len(lines):
            break
        line = lines[i]
        while line != '':
            if line == '\0':
                flag = False
                break
            text += line
            i += 1
            if i >= len(lines):
                break
            line = lines[i]
        return_list.append(text)
    return return_list


if __name__ == '__main__':
    easyocr_text = open('text_output_tesseract.txt', 'r')
    true_text = open('true_text_easyocr_all.txt', 'r')
    # easyocr_text = open('text_output_easyocr_all.txt', 'r')
    # true_text = open('true_text_easyocr_all1.txt', 'r')
    whole_output = easyocr_text.read()
    whole_true = true_text.read()
    easy_texts = read_texts(whole_output.splitlines())
    true_texts = read_texts(whole_true.splitlines())
    print(easy_texts)
    print(true_texts)
    acc = 0
    for j in range(423):
        acc += levenshtein_accuracy(easy_texts[j], true_texts[j])

    print('{0:.2f}%'.format((acc / 423) * 100))
    print('{0:.2f}%'.format(levenshtein_accuracy(whole_output, whole_true) * 100))
