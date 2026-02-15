# Marvel vs DC: Análise de NLP em Comunidades Digitais

## Sobre o Projeto
Análise comparativa do comportamento de fãs da Marvel e DC no YouTube (2020-2025) utilizando Processamento de Linguagem Natural (NLP). O objetivo da pesquisa é entender se as bases de fãs possuem dinâmicas sociais distintas e como reagem a fatores externos, como campanhas de marketing e polêmicas do mundo real.

## Tecnologias Utilizadas
* **Linguagem:** Python
* **NLP & Machine Learning:** BERTopic (SBERT, c-TF-IDF), NLTK, Scikit-Learn
* **Coleta de Dados:** YouTube Data API v3
* **Visualização:** Plotly, WordCloud, Matplotlib

## Principais Descobertas
* **Marvel:** Foco no "Macro" (Universo Expandido). O engajamento é guiado por memes, consumo rápido (Geração Z) e uma forte blindagem institucional contra polêmicas de atores.
* **DC :** Foco no "Micro" (o filme isoladamente). Discussões mais politizadas, focadas em estética/atuação e com alta vulnerabilidade a polêmicas reais ("Tribunal da Internet").
* **Convergência:** Ambas as comunidades apresentam sinais claros de saturação/fadiga com o gênero de super-heróis e excesso de exposição nos trailers.
* Informações complementares disponíveis no arquivo "relatorio_final.ipynb". Além disso, imagens dos tópicos principais utilizados para análise também estão neste repositório.

## Como Executar
1. Clone este repositório: `git clone https://github.com/seu-usuario/seu-repositorio.git`
2. Instale as dependências: `pip install bertopic nltk scikit-learn plotly wordcloud`
3. Execute o notebook `relatorio_final.ipynb` (via Jupyter ou Google Colab).
4. O notebook contém uma célula configurável no final do arquivo para gerar gráficos dinâmicos de qualquer tópico analisado.
