import streamlit as st
import pandas as pd
import io

def parse_penset(txt):
    # Jednoduché parsování podle tebou dodaného formátu
    lines = txt.strip().split('\n')
    data_lines = []
    start = False
    for line in lines:
        if line.startswith("Index"):
            start = True
            continue
        if start:
            if line.strip() == '':
                break
            data_lines.append(line)

    # Převod na DataFrame
    rows = []
    for line in data_lines:
        parts = line.split('\t')
        if len(parts) >= 7:
            rows.append({
                'Index': parts[0],
                'Červená': parts[1],
                'Zelená': parts[2],
                'Modrá': parts[3],
                'Tloušťka (v mm)': parts[4],
                'Používá se': parts[5],
                'Popis': parts[6]
            })
    return pd.DataFrame(rows)

st.title("Pen set editor")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)
    st.write("Načtená data:")
    st.dataframe(df)
