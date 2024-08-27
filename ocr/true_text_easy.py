import os

import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('annot.csv', encoding_errors='ignore')
    ids = [img.split('.')[0] for img in os.listdir('./images/')]

    id_df = df.groupby('image_id')
    print(list(id_df))
    #
    # true_output = open('true_text_easyocr.txt', 'w', errors='ignore')
    # i = 0
    # for ID in ids:
    #     print(i)
    #     i += 1
    #     filtered_rows = id_df.get_group(ID)
    #     text = list(filtered_rows['utf8_string'])
    #     text.sort()
    #     true_output.write('\n'.join(text))
    #     true_output.write('\n')
    #     true_output.write('\n')
    # true_output.close()
