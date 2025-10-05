from pypdf import PdfReader
def pdf_reader(file):
    print('Lendo o arquivo pdf...')
    reader = PdfReader(f'{file}')
    full_text = ''
    for page in range(len(reader.pages)):
        current_page = reader.pages[page]
        text = current_page.extract_text()
        full_text += text
    return full_text
