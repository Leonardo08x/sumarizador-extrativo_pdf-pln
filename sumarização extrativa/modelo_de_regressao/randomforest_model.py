import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import glob
from sklearn.metrics import mean_absolute_error
def buscar_excels():
    print
    banco_de_dados = glob.glob(r"banco de dados/*.xlsx")

    return banco_de_dados
def concatenar_dados(banco_de_dados):
    print('Concatenando dados dos arquivos Excel...')
    lista_dfs = []
    for arquivo in banco_de_dados:
        df_atual = pd.read_excel(arquivo)
        lista_dfs.append(df_atual)
    print('Dados concatenados com sucesso.')
    df_concatenado = pd.concat(lista_dfs, ignore_index=True)
    return df_concatenado
def modelo_de_aprendizado(dados_para_regressao):
    print('Iniciando o modelo de aprendizado de máquina...')
    banco_de_dados = buscar_excels()
    df_concatenado = concatenar_dados(banco_de_dados)
    print('Dados concatenados:')
    print(df_concatenado.head())
    # etapa de treino
    print('Preparando dados para treino...')
    y = df_concatenado['Pontos Refinados']
    features = ['Score', 'posição da Sentença','Substantivos', 'Verbos', 'Adjetivos', 'Pronomes', 'Advérbios']
    X = df_concatenado[features]
    train_X, val_X, train_y, val_y = train_test_split(X, y,random_state = 0)
    forest_model = RandomForestRegressor(random_state=1)
    forest_model.fit(train_X, train_y)
    val_predictions = forest_model.predict(val_X)
    print('previsão do set de validação:')
    print(val_predictions)
    print('Mean Absolute Error do set de validação:')
    print(mean_absolute_error(val_y, val_predictions))
    print('Aplicando o modelo aos novos dados...')
    X = dados_para_regressao[features]
    predicted_scores = forest_model.predict(X)
    print('previsão dos novos dados:')
    print(predicted_scores)
    dados_para_regressao['Pontos Refinados'] = predicted_scores
    dados_para_regressao.to_excel('banco de dados previstos/resultados_da_regressão.xlsx', index=False)
    return predicted_scores