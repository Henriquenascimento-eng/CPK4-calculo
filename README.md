# Checkpoint 4 — Limites, Desempenho de APIs e Streamlit

Análise do tempo de resposta de uma API em função da carga de requisições por segundo,
utilizando limites para investigar a região crítica de saturação do sistema, com
implementação em Python/SymPy e aplicação interativa em Streamlit.

**Modelo matemático:** `T(x) = 1000 / (50 - x)`, onde `x` é a carga em req/s e `T(x)` é o
tempo médio de resposta previsto, em ms.

## Conteúdo do repositório

- `checkpoint.ipynb` — notebook principal: relatório técnico, desenvolvimento matemático,
  cálculo dos limites, implementação, simulações, gráficos e geração do `app.py`.
- `app.py` — aplicação Streamlit (gerada a partir do notebook; usa o mesmo modelo).
- `requirements.txt` — dependências do projeto.
- `grafico_modelo.png` — gráfico exportado pelo notebook (gerado ao executar as células).

## Como instalar as dependências

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
py -m pip install streamlit
py -m pip install pandas
py -m pip install matplotlib

```

## Como executar o notebook

```bash
jupyter notebook checkpoint.ipynb
```

Execute todas as células em ordem (Run All / Executar tudo). A última seção de código do
notebook gera automaticamente o arquivo `app.py` na mesma pasta.

## Como executar a aplicação Streamlit

```bash
py -m pip install streamlit
```

Isso abrirá a aplicação no navegador, permitindo ajustar a carga de requisições por
segundo e visualizar o tempo de resposta previsto, a região crítica e a assíntota do
modelo.

## RMs
-- Henrique S. S. Nascimento - rm569137
--Nicolas Moreira - rm571510
--Andrey Luigi - rm569575
--Lucas Trevisan - rm569731


