# Sumarizador Extrativo de Documentos PDF

## Visão Geral do Projeto

Este projeto consiste na implementação de um sistema de **Sumarização Extrativa de Textos** contidos em arquivos PDF, utilizando técnicas de **Processamento de Linguagem Natural (PLN)** e a biblioteca **spaCy** para análise linguística em português. O objetivo principal é gerar resumos automáticos e coerentes que preservem as frases mais relevantes do documento original, conforme determinado pela pontuação de frequência de lemas-chave.

A interface gráfica do usuário (GUI) foi desenvolvida com **PyQt6** para facilitar a interação, permitindo que o usuário selecione um arquivo PDF, visualize o texto bruto e obtenha o resumo final de forma intuitiva.

---

## Estrutura Acadêmica

Este trabalho é uma atividade de apresentação de **Bolsa de Iniciação Científica (IC)** e está vinculado ao **Curso de Ciência da Computação** do **Instituto de Ciências Exatas e Naturais (ICEN)** da **Faculdade de Computação (FACOMP)** da **Universidade Federal do Pará (UFPA)**.

* **Instituição:** Universidade Federal do Pará (UFPA)
* **Orientadora:** Profa. Dra. Paula Christina Figueira Cardoso

---

## Pipeline de Sumarização e Modularização

O sistema segue um pipeline modular dividido em etapas lógicas, garantindo escalabilidade e facilidade de manutenção:

### Módulos de Utilidade (`utils/`)

* `pdf_reader.py`: Responsável pela leitura e extração do texto completo do arquivo PDF.
* `tokenizer.py`: Utiliza o spaCy (`pt_core_news_lg`) para processar o texto, realizando a **separação em sentenças** e a tokenização avançada (obtendo **lema**, **POS** e **is_stop**), preservando a estrutura de frases.

### Módulo de Sumarização (`sumarizacao/`)

* `sumarizador.py`: Contém a lógica central da sumarização extrativa:
    * `pontuador_de_lemmas()`: Calcula o peso (frequência normalizada) de palavras-chave (Substantivos, Nomes Próprios e Adjetivos).
    * `puntuador_de_sentencas()`: Pontua cada frase somando os pesos dos lemas que ela contém.
    * `extracao_das_melhores_sentencas()`: Seleciona as frases mais bem pontuadas e as reordena na sequência original do texto para gerar o resumo final.

### Interface Principal (`main_ipqt6.py`)

* Contém a interface gráfica **PyQt6** para a interação do usuário.
* Gerencia a execução do pipeline de sumarização em uma **thread separada** para evitar travamento da GUI.

---

## Requisitos e Instalação

Para rodar o projeto, você precisará do Python 3.8+ e das seguintes bibliotecas:

```bash
pip install spacy PyQt6 PyPDF2
python -m spacy download pt_core_news_lg
