import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Mesmo modelo matemático desenvolvido e validado no notebook (checkpoint.ipynb):
#   T(x) = 1000 / (50 - x)
# onde x = requisições por segundo e T(x) = tempo médio de resposta (ms).
# Ajustado a partir dos dados do teste de carga fornecido pela equipe de Engenharia.
# ---------------------------------------------------------------------------
CAPACIDADE_TEORICA = 50       # req/s -- ponto de assintota vertical do modelo
LIMITE_SEGURO = 45            # req/s -- inicio da regiao critica (90% da capacidade teorica)
SLA_LATENCIA_MS = 150         # ms -- referencia de desempenho (SLA) usada na discussao


def tempo_resposta(carga_req_s: float) -> float:
    """Tempo medio de resposta previsto pelo modelo, em milissegundos."""
    return 1000 / (CAPACIDADE_TEORICA - carga_req_s)


st.set_page_config(page_title="Desempenho da API vs. Carga", layout="centered")

st.title("Desempenho da API sob carga de requisicoes")
st.markdown(
    """
Esta aplicacao usa o modelo matematico $T(x) = 1000 / (50 - x)$, desenvolvido no
notebook do Checkpoint 4, para prever o **tempo medio de resposta** da API (em ms) de
acordo com a **carga de requisicoes por segundo (req/s)**.

A infraestrutura atual tem capacidade teorica estimada em **50 req/s** -- ponto em que o
modelo apresenta uma assintota vertical (tempo de resposta tende ao infinito).
"""
)

carga = st.slider(
    "Requisicoes por segundo (req/s)",
    min_value=0.0,
    max_value=49.9,
    value=30.0,
    step=0.1,
    help="Escolha a carga de requisicoes por segundo para simular o tempo de resposta.",
)

tempo_previsto = tempo_resposta(carga)

col1, col2 = st.columns(2)
col1.metric("Carga escolhida", f"{carga:.1f} req/s")
col2.metric("Tempo de resposta previsto", f"{tempo_previsto:.1f} ms")

if carga >= LIMITE_SEGURO:
    st.error(
        f"Carga dentro da regiao critica (>= {LIMITE_SEGURO} req/s, "
        f"{LIMITE_SEGURO/CAPACIDADE_TEORICA:.0%} da capacidade teorica). "
        "O tempo de resposta cresce muito rapidamente nesta faixa -- risco alto de "
        "estourar SLA e comprometer a disponibilidade do sistema."
    )
elif tempo_previsto > SLA_LATENCIA_MS:
    st.warning(
        f"O tempo de resposta previsto ({tempo_previsto:.1f} ms) ja ultrapassa o "
        f"SLA de latencia de referencia ({SLA_LATENCIA_MS} ms)."
    )
else:
    st.success(
        f"Carga dentro de uma faixa operacional considerada saudavel "
        f"(tempo de resposta abaixo do SLA de {SLA_LATENCIA_MS} ms)."
    )

# --- grafico ---------------------------------------------------------------
x_vals = np.linspace(0, 49.9, 1000)
y_vals = 1000 / (CAPACIDADE_TEORICA - x_vals)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x_vals, y_vals, color="#2563eb", linewidth=2, label="Modelo T(x) = 1000/(50-x)")
ax.axvline(CAPACIDADE_TEORICA, color="#dc2626", linestyle="--", label="Assintota vertical (50 req/s)")
ax.axvspan(LIMITE_SEGURO, CAPACIDADE_TEORICA, color="#fecaca", alpha=0.4, label="Regiao critica")
ax.axhline(SLA_LATENCIA_MS, color="#059669", linestyle=":", label=f"SLA de referencia ({SLA_LATENCIA_MS} ms)")
ax.scatter([carga], [tempo_previsto], color="#111827", zorder=5, s=60, label="Carga selecionada")

ax.set_xlim(0, 51)
ax.set_ylim(0, max(600, tempo_previsto * 1.2))
ax.set_xlabel("Requisicoes por segundo (req/s)")
ax.set_ylabel("Tempo medio de resposta (ms)")
ax.set_title("Tempo de resposta previsto vs. carga de requisicoes")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)

st.markdown(
    """
---
**Como ler este grafico:** a curva mostra como o tempo de resposta se comporta conforme a
carga aumenta. A linha vermelha tracejada marca a capacidade teorica do sistema (50 req/s),
onde o modelo diverge para o infinito. A faixa vermelha clara marca a regiao critica, onde
operar traz risco operacional real, mesmo que ainda seja "matematicamente possivel".
"""
)
