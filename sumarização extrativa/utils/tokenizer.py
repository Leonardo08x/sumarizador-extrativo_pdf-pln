import spacy
def tokenizer_spacy(doc_text):
    print('Tokenizando com spacy...')
    nlp =  spacy.load("pt_core_news_lg")
    tokenized_text = nlp(doc_text)
    tokenized_sents = []
    for sent in tokenized_text.sents:
        current_sent = []
        for token in sent:
           current_sent.append([token.text, token.lemma_, token.pos_, token.dep_, token.is_stop])
        tokenized_sents.append(current_sent)
    return tokenized_sents