import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv('new__out.csv', encoding_errors='ignore')
    ids = [
        '000a1a700c0c7950',
        '000aecd78b230135',
        '000bd0b4fa27644c',
        '000ca4a1855318b1',
        '000ed967c71e566f',
        '0002c799b0cd7412',
        '0002cb8d8ea5eb7e',
        '0002f9c7fac5f093',
        '00c359f294f7dcd9',
        '01aa9b9a3520fc0c'
    ]

    id_df = df.groupby('id')
    true_output = open('true_text_easyocr.txt', 'w', errors='ignore')
    for ID in ids:
        filtered_rows = id_df.get_group(ID)
        text = list(filtered_rows['text'])
        text.sort()
        true_output.write(ID + '\n')
        true_output.write('\n'.join(text))
        true_output.write('\n')
        true_output.write('\n')
    true_output.close()
