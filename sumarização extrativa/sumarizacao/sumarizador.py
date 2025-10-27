import datetime
from modelo_de_regressao.randomforest_model import modelo_de_aprendizado

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

def extração_das_melhores_sentencas(tokens, sent_scores,modo_de_operação):
    print('Extraindo as melhores sentenças...')
    total_de_sentencas_para_extracao = round(0.4 * len(tokens))
    sent_scores_sorted = sort_dict_by_value(sent_scores)
    print(f'Total de sentenças para extração: {total_de_sentencas_para_extracao}')
    string_final = ''
    lista_pos_processamento = []
    for i in range(total_de_sentencas_para_extracao):
        frase_atual = []
        frase_atual_sem_tokens= ''
        for j in tokens[list(sent_scores_sorted.keys())[i]]:
            string_final += j[0] + ' '
            frase_atual.append(j)
            frase_atual_sem_tokens += j[0] + ' '
        lista_pos_processamento.append([frase_atual, sent_scores_sorted[list(sent_scores_sorted.keys())[i]],list(sent_scores_sorted.keys())[i], frase_atual_sem_tokens])
        string_final += '\n'
    pos_processamento(lista_pos_processamento, modo_de_operação)
    return string_final

def pos_processamento(lista_pos_processamento,modo_de_operação):
    print('Iniciando o pós-processamento...')
    dados_para_df,dados_para_regressao = [],[]
    for tokens in lista_pos_processamento:
        substantivos,verbos,adjetivos,pronomes,advérbios  = 0,0,0,0,0
        for token in tokens[0]:
           if token[0] != '\n': 
            if token[2] == 'NOUN' or token[2] == 'PROPN':
                substantivos +=1
            if token[2] == 'VERB':
                verbos +=1
            if token[2] == 'ADJ':
                adjetivos +=1
            if token[2] == 'PRON':
                pronomes +=1
            if token[2] == 'ADV':
                advérbios +=1
        pontos_refinados = ((substantivos + verbos + adjetivos + pronomes + advérbios)*(tokens[1]/tokens[2]))/(len(tokens[0])*tokens[2])
        dados_para_df.append([tokens[3], tokens[1],tokens[2], substantivos, verbos, adjetivos, pronomes, advérbios, pontos_refinados])
        dados_para_regressao.append([tokens[3], tokens[1],tokens[2],substantivos, verbos, adjetivos, pronomes, advérbios])
    if modo_de_operação == 'excel':
        salvamento_em_excel(dados_para_df)
    elif modo_de_operação == 'regressão':
        import pandas as pd
        dados_para_regressao_df = pd.DataFrame(dados_para_regressao, columns=['Frase', 'Score', 'posição da Sentença', 'Substantivos', 'Verbos', 'Adjetivos', 'Pronomes', 'Advérbios'])
        print(dados_para_regressao_df)
        modelo_de_aprendizado(dados_para_regressao_df)

def salvamento_em_excel(dados_para_df):    
    import pandas as pd
    from datetime import datetime
    df = pd.DataFrame(dados_para_df, columns=['Frase', 'Score', 'posição da Sentença', 'Substantivos', 'Verbos', 'Adjetivos', 'Pronomes', 'Advérbios', 'Pontos Refinados'])
    utc_dt = datetime.now()
    hora_local_formatada = utc_dt.strftime("%d-%m-%Y,%H-%M-%S")
    df.to_excel(f'banco de dados/pos_processamento_{hora_local_formatada}.xlsx', index=False)
    print(df)
