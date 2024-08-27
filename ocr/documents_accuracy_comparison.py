import os
import pytesseract
from PIL import Image
from easyocr import Reader
import Levenshtein
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']


def get_text_from_google_doc(doc_id):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and  creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError('credentials.json file not found.')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)
    document = service.documents().get(documentId=doc_id).execute()
    content = document.get('body').get('content')

    text = ''

    for element in content:
        if 'paragraph' in element:
            elements = element.get('paragraph').get('elements')
            for elem in elements:
                if 'textRun' in elem:
                    text += elem.get('textRun').get('content')

    return text


def levenshtein_accuracy(ocr_text, actual_text):
    distance = Levenshtein.distance(ocr_text, actual_text)
    max_length = max(len(actual_text), len(ocr_text))
    accuracy = (max_length - distance) / max_length
    return accuracy


if __name__ == '__main__':
    document_ids = ['1s9YakEmg4rza_8fW_GriE5K0aUOG_5KENzz0lwHrmt0', '1FFdfIvhcX_K73PuaMNA09539W0aBYLDdzX71HDCNnT0',
                    '1CI-x4_KobW-0EV1EguQ_ZpdyT2K0V9nLg73zJx-KGeE', '1_136_pY9OhX7JXcFABjt-UMkKPxV6J8zkrawYJw-MEM',
                    '1HOng_ytPX4DZfLs79rO7uYG_rwRfugOMe9MrJ2eUfwA', '1HiaWXXbGe1FlscIq2t4j8Vyz0Aih6nvsBye1O-jsqPk',
                    '1luOyz0e8YF-Jxhe2beLLwJ8E8rKUSqGaubRmzi7rqak', '19IfCFZJwVh_kqU86eTcNnN_nXxf_nmp2_MP_L46Q1TQ',
                    '1nIXucqeVtxaaxwugR5V29oaSRuzV7w6wbdjnFT19RQU', '1Uw7rk1t2p5kSqxI-uPi5dTn5Y16O5zb3wRNO1MMjRgc']
    reader = Reader(['en'])
    source_folder = './dokumenti_dpns/'
    image_fns = [file for file in os.listdir('./dokumenti_dpns/')[:10]]
    zbir1 = 0
    zbir2 = 0
    for id in document_ids:
        actual = get_text_from_google_doc(id)
        image = Image.open(source_folder + id + '.png')
        tesseract_data = pytesseract.image_to_string(lang='eng', image=image)
        easy_data = reader.readtext(source_folder + id + '.png')
        easy_text = ''
        for res in easy_data:
            easy_text += res[1]
            easy_text += '\n'
        acc = levenshtein_accuracy(tesseract_data.lower(), actual.lower())
        acc2 = levenshtein_accuracy(easy_text.lower(), actual.lower())
        zbir1 += acc
        zbir2 += acc2

    prosek1 = zbir1 / len(document_ids)
    prosek2 = zbir2 / len(document_ids)
    print(f"Tesseract average accuracy: {prosek1:.2f}")
    print(f"EasyOCR average accuracy: {prosek2:.2f}")
