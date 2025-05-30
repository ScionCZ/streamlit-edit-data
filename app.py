import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Pen set editor", layout="wide")

def parse_penset(txt):
    lines = txt.strip().split('\n')
    data_lines = []
    start = False
    for line in lines:
        if line.startswith("Index"):
            start = True
            continue
        if start:
            if line.strip() == '' or set(line.strip()) == {'*'}:
                continue
            data_lines.append(line)

    rows = []
    for line in data_lines:
        parts = line.split('\t')
        if len(parts) >= 7:
            try:
                rows.append({
                    'Index': int(parts[0]),
                    'Červená': int(parts[1]),
                    'Zelená': int(parts[2]),
                    'Modrá': int(parts[3]),
                    'Barva': f"#{int(parts[1]):02x}{int(parts[2]):02x}{int(parts[3]):02x}",
                    'Tloušťka (v mm)': float(parts[4]),
                    'Používá se': parts[5],
                    'Popis': parts[6]
                })
            except ValueError:
                continue
    return pd.DataFrame(rows)

def dataframe_to_txt(df):
    lines = ["---- PERA (2-TLČ) ----", "Index\tČervená\tZelená\tModrá\tTloušťka (v mm)\tPoužívá se\tPopis", "*****\t*****\t*****\t*****\t*****\t*****\t*****"]
    for _, row in df.iterrows():
        line = f"{row['Index']}\t{row['Červená']}\t{row['Zelená']}\t{row['Modrá']}\t{row['Tloušťka (v mm)']:.6f}\t{row['Používá se']}\t{row['Popis']}"
        lines.append(line)
    return '\n'.join(lines)

st.title("Pen set editor")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)

    # Zobrazit tabulku s barevným náhledem vedle RGB
    styled_df = df.copy()
    styled_df.insert(4, "Náhled", [f"""
        <div style='width: 30px; height: 20px; background-color: {color}; border: 1px solid #000;'></div>
        """ for color in df['Barva']], allow_duplicates=True)

    st.write("### Načtená data s náhledem barev:")
    st.write("Pozn.: Náhledy barev jsou vloženy za sloupec 'Modrá'.")
    st.write("\n")
    st.write("Barvu lze editovat změnou RGB hodnot v tabulce nebo pomocí budoucích nástrojů.")

    st.write("\n")
    st.write("Aktualizovaná tabulka:")
    st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Tlačítko pro export
    st.write("\n")
    if st.button("Exportovat jako .txt", type="primary"):
        txt_output = dataframe_to_txt(df)
        st.download_button("Stáhnout .txt soubor", data=txt_output, file_name="exported_penset.txt", mime="text/plain")
