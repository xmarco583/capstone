import streamlit as st
import joblib

# Áreas en orden
areas = [
    'CCFM', 'CCSS', 'CCNA', 'CCCO', 'ARTE', 'BURO',
    'CCEP', 'IIAA', 'FINA', 'LING', 'JURI'
]


column_items = {}
for idx, area in enumerate(areas):
    items = [idx + 1 + 13 * i for i in range(11)]  # p1, p14, ..., p131 (1-based)
    column_items[area] = [n-1 for n in items]  # 0-based

row_items = {}
for idx, area in enumerate(areas):
    start = idx*11 + 1
    end = start + 11
    items = list(range(start, end))
    row_items[area] = [n-1 for n in items]  # 0-based

def calcular_puntajes_directos(respuestas):
    """Devuelve una lista de 11 puntajes directos en el orden de las áreas."""
    puntajes = []
    for area in areas:
        a_count = sum(respuestas[i] == 'a' or respuestas[i] == 'ambas' for i in column_items[area])
        b_count = sum(respuestas[i] == 'b' or respuestas[i] == 'ambas' for i in row_items[area])
        puntajes.append(a_count + b_count)
    return puntajes

# --- Interfaz Streamlit ---
st.title("Test Vocacional - Predicción por modelo")

preguntas = [f"Pregunta {i}" for i in range(1, 144)]
respuestas = [st.radio(texto, ['a', 'b', 'ambas'], key=f"preg_{i}") for i, texto in enumerate(preguntas, 1)]

if st.button("Predecir perfil vocacional"):
    puntajes = calcular_puntajes_directos(respuestas)
    modelo = joblib.load('modelo_rf.pkl')
    le = joblib.load('label_encoder.pkl')
    area_predicha = le.inverse_transform(modelo.predict([puntajes]))[0]
    st.success(f"Área vocacional dominante predicha por el modelo: **{area_predicha}**")
    st.write("Puntajes directos usados:", dict(zip(areas, puntajes)))