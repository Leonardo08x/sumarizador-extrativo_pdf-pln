# Sumarizador Extrativo de Documentos PDF

## Visão Geral do Projeto

Este projeto consiste na implementação de um sistema de **Sumarização Extrativa de Textos** contidos em arquivos PDF, utilizando técnicas de **Processamento de Linguagem Natural (PLN)** e a biblioteca **spaCy** para análise linguística em português.

O sistema opera com modos de operação definidos:
1.  **Modo Extrativo (Base):** Gera o resumo selecionando as frases mais relevantes pela pontuação de frequência de lemas-chave.
2.  **Modo 'regressão':** Utiliza as features linguísticas extraídas em um modelo de **Regressão** para refinar a seleção e pontuação das sentenças.
3.  **Modo 'excel':** Exporta as features linguísticas e scores para um arquivo Excel para análise e criação de *datasets*.

A interface gráfica do usuário (GUI) foi desenvolvida com **PyQt6** para facilitar a interação.

---

Este trabalho é uma atividade da **Bolsa de Iniciação Científica (IC)** e está vinculado ao **Curso de Ciência da Computação** do **Instituto de Ciências Exatas e Naturais (ICEN)** da **Faculdade de Computação (FACOMP)** da **Universidade Federal do Pará (UFPA)**.

* **Instituição:** Universidade Federal do Pará (UFPA)
* **Autor:** Leonardo Cunha da Rocha
* **Orientadora:** Profa. Dra. Paula Christina Figueira Cardoso

---

## Pipeline de Sumarização e Modularização

O sistema segue um pipeline modular dividido em etapas lógicas:

### Módulos de Utilidade (`utils/`)

* `pdf_reader.py`: Responsável pela leitura e extração do texto completo do arquivo PDF.
* `tokenizer.py`: Utiliza o spaCy (`pt_core_news_lg`) para processar o texto, realizando a **separação em sentenças** e a tokenização avançada (obtendo **lema**, **POS** e **is_stop**).

### Módulo de Sumarização (`sumarizacao/`)

* `sumarizador.py`: Contém a lógica central da sumarização extrativa:
    * `pontuador_de_lemmas()`: Calcula o peso (frequência normalizada) de palavras-chave (Substantivos, Nomes Próprios e Adjetivos).
    * `puntuador_de_sentencas()`: Pontua cada frase somando os pesos dos lemas que ela contém.
    * `extracao_das_melhores_sentencas()`: Seleciona uma porcentagem das frases (atualmente 40%) com maior score base e as encaminha para o Pós-Processamento.
    * **`pos_processamento()`:** Módulo crucial que extrai features linguísticas (contagem de Substantivos, Verbos, Adjetivos, Pronomes, Advérbios) para cada sentença e executa a operação final baseada no `modo_de_operação`:
        * **Modo 'excel':** Executa `salvamento_em_excel()` para exportar o *dataset* completo (frase, score base e features).
        * **Modo 'regressão':** Executa `modelo_de_aprendizado()` no módulo de Regressão, usando as features extraídas.

### Módulo de Regressão (`modelo_de_regressao/`)

* `randomforest_model.py`: Contém a função `modelo_de_aprendizado()` responsável por carregar e aplicar o modelo de regressão (como Random Forest) para gerar novos scores de relevância para as sentenças, refinando a sumarização.

### Interface Principal (`main_ipqt6.py`)

* Contém a interface gráfica **PyQt6** para a interação do usuário.
* Gerencia a execução do pipeline em uma **thread separada**.

---

## Requisitos e Instalação

Para rodar o projeto, você precisará do Python 3.8+ e das seguintes bibliotecas:

```bash
# Adicionado pandas (para manipulação de DataFrame e Excel) e bibliotecas de ML (scikit-learn)
pip install spacy PyQt6 PyPDF2 pandas scikit-learn
python -m spacy download pt_core_news_lg
