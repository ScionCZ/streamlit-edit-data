import streamlit as st
import pandas as pd

# Data z tvého příkladu
data = {
    "Index": [1, 2, 3, 4, 5],
    "Červená": [0, 127, 255, 2, 64],
    "Zelená": [0, 127, 102, 158, 165],
    "Modrá": [0, 127, 0, 33, 255],
    "Tloušťka (v mm)": [0.13, 0.15, 0.18, 0.20, 0.25],
    "Používá se": ["Používá se", "Používá se", "Používá se", "Používá se", "Používá se"],
    "Popis": [
        "Obecné - výplně",
        "2D prvky - obecné",
        "Výplně otvorů - obecné",
        "Objekty - obecné",
        "Anotace - obecné",
    ],
}

df = pd.DataFrame(data)

st.title("Editor dat PERA (2-TLČ)")

edited_df = st.data_editor(df, num_rows="dynamic")

st.write("Upravená data:")
st.dataframe(edited_df)
