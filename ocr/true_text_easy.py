import pandas as pd
from new_ids import ids

if __name__ == '__main__':
    df = pd.read_csv('new__out.csv', encoding_errors='ignore', na_values=None, keep_default_na=False)

    # Samo za desettee sliki koi ze vo dokumentacijata
    # id_df = df.groupby('id')
    # print([ID.split('_')[2].split('.')[0] for ID in ids[:10]])

    # Site sliki koi imaat entry vo new__out.csv
    # ids = df['id'].unique()
    id_df = df.groupby('id')
    # print(list(ids))
    # print(len(ids))

    true_output = open('true_text_easyocr.txt', 'w', errors='ignore')
    # true_output = open('true_text_easyocr_all.txt', 'w', errors='ignore')
    i = 0
    for ID in ids:
        print(i)
        i += 1
        filtered_rows = id_df.get_group(ID)
        text = list(filtered_rows['text'])
        print(text)
        text.sort()
        true_output.write('\n'.join(text))
        true_output.write('\n')
        true_output.write('\n')
    true_output.close()
