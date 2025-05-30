import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Pen Set Editor", layout="wide")

st.title("Pen set editor")

# Funkce pro parsování .txt souboru
def parse_penset(txt):
    lines = txt.strip().split('\n')
    data_lines = []
    start = False
    for line in lines:
        if line.startswith("Index"):
            start = True
            continue
        if start:
            if line.strip() == '' or line.startswith("*****"):
                continue
            data_lines.append(line)

    rows = []
    for line in data_lines:
        parts = line.split('\t')
        if len(parts) >= 7:
            rows.append({
                'Index': parts[0],
                'Červená': int(parts[1]),
                'Zelená': int(parts[2]),
                'Modrá': int(parts[3]),
                'Tloušťka (v mm)': float(parts[4]),
                'Používá se': parts[5],
                'Popis': parts[6]
            })
    return pd.DataFrame(rows)

# Funkce pro generování barevného náhledu
def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)

    st.subheader("Uprav data")

    edited_rows = []
    for i, row in df.iterrows():
        st.markdown(f"#### Položka {row['Index']}")
        cols = st.columns([1, 1, 1, 1, 2, 3, 1])

        r = cols[0].number_input("Červená", min_value=0, max_value=255, value=int(row['Červená']), key=f"r_{i}")
        g = cols[1].number_input("Zelená", min_value=0, max_value=255, value=int(row['Zelená']), key=f"g_{i}")
        b = cols[2].number_input("Modrá", min_value=0, max_value=255, value=int(row['Modrá']), key=f"b_{i}")

        thickness = cols[3].number_input("Tloušťka (v mm)", value=float(row['Tloušťka (v mm)']), key=f"t_{i}")
        desc = cols[4].text_input("Popis", value=row['Popis'], key=f"d_{i}")

        hex_color = rgb_to_hex(r, g, b)
        cols[5].markdown(f'<div style="width:100%; height:38px; background-color:{hex_color}; border-radius:5px; border:1px solid #ccc"></div>', unsafe_allow_html=True)

        edited_rows.append({
            'Index': row['Index'],
            'Červená': r,
            'Zelená': g,
            'Modrá': b,
            'Tloušťka (v mm)': thickness,
            'Používá se': row['Používá se'],
            'Popis': desc
        })

    edited_df = pd.DataFrame(edited_rows)

    st.subheader("Exportovat změny")
    if st.button("📥 Exportovat jako .txt", type="primary"):
        output = io.StringIO()
        output.write("---- PERA (2-TLČ) ----\n")
        output.write("Index\tČervená\tZelená\tModrá\tTloušťka (v mm)\tPoužívá se\tPopis\n")
        output.write("*****\t*****\t*****\t*****\t*****\t*****\t*****\n")
        for _, row in edited_df.iterrows():
            output.write(f"{row['Index']}\t{row['Červená']}\t{row['Zelená']}\t{row['Modrá']}\t{row['Tloušťka (v mm)']:.6f}\t{row['Používá se']}\t{row['Popis']}\n")
        st.download_button("Stáhnout soubor", data=output.getvalue(), file_name="upraveny_penset.txt", mime="text/plain")
