def pontuador_de_lemmas(tokens):
    print('Pontuando lemas...')
    lemma_dict = {}
    for sent in tokens:
        for word in sent:
           if word[2] in ['NOUN', 'PROPN', 'ADJ'] and not word[4]:
                if word[1] not in lemma_dict:
                    lemma_dict[word[1]] = 1
                else:
                    lemma_dict[word[1]] += 1
    return lemma_dict

def puntuador_de_sentencas(tokens, lemma_dict):
    print('Pontuando sentenças...')
    sent_scores = {}
    for sent in range(len(tokens)):
        current_score = 0
        for word in tokens[sent]:
            if word[1] in lemma_dict:
                current_score += lemma_dict[word[1]]
        sent_scores[sent] = current_score

    return sent_scores

def sort_dict_by_value(dict_to_sort):
    print('Ordenando dicionário por valor...')
    dict_to_tuple = list(zip(dict_to_sort.keys(), dict_to_sort.values()))
    dict_to_tuple.sort(key=lambda x: x[1], reverse=True)
    return {k: v for k, v in dict_to_tuple}

def extração_das_melhores_sentencas(tokens, sent_scores):
    print('Extraindo as melhores sentenças...')
    total_de_sentencas_para_extracao = round(0.4 * len(tokens))
    sent_scores_sorted = sort_dict_by_value(sent_scores)
    print(f'Total de sentenças para extração: {total_de_sentencas_para_extracao}')
    string_final = ''
    for i in range(total_de_sentencas_para_extracao):
        for i in tokens[list(sent_scores_sorted.keys())[i]]:
            string_final += i[0] + ' '
        string_final += '\n'
    return string_final
