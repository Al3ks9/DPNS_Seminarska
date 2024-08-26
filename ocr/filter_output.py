if __name__ == '__main__':
    original_file = 'true_text_easyocr_all.txt'
    new_file = 'true_text_easyocr_all1.txt'

    with open(original_file, 'r') as file:
        lines = file.readlines()

    with open(new_file, 'w') as file:
        for line in lines:
            print(line)
            if line.strip() != ".":
                file.write(line)
