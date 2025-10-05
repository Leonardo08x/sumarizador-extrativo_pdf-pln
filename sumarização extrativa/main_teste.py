from utils.pdf_reader import pdf_reader
from utils.tokenizer import tokenizer_spacy
from sumarizacao.sumarizador import pontuador_de_lemmas, puntuador_de_sentencas, extração_das_melhores_sentencas

def main(file):
    print('Iniciando o processo de sumarização extrativa...')
    doc_text = pdf_reader(file)
    tokens = tokenizer_spacy(doc_text)
    dict_lemmas_pontuados = pontuador_de_lemmas(tokens)
    dict_sentencas_pontuados = puntuador_de_sentencas(tokens, dict_lemmas_pontuados)
    string_final = extração_das_melhores_sentencas(tokens, dict_sentencas_pontuados)
    print(string_final)

main("arquivo_de_teste.pdf")
