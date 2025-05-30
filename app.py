import streamlit as st
import pandas as pd
import io

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

def df_to_penset(df):
    lines = []
    lines.append("---- PERA (2-TLČ) ----")
    lines.append("Index\tČervená\tZelená\tModrá\tTloušťka (v mm)\tPoužívá se\tPopis")
    lines.append("*****\t*****\t*****\t*****\t*****\t*****\t*****")
    for _, row in df.iterrows():
        lines.append(f"{row['Index']}\t{row['Červená']}\t{row['Zelená']}\t{row['Modrá']}\t{row['Tloušťka (v mm)']:.6f}\t{row['Používá se']}\t{row['Popis']}")
    return '\n'.join(lines)

st.title("Pen set editor")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)

    st.write("Načtená data:")
    edited_df = st.data_editor(
        df,
        column_config={
            "Index": st.column_config.TextColumn(disabled=True),
            "Používá se": st.column_config.TextColumn(disabled=True),
        },
        use_container_width=True,
        num_rows="dynamic"
    )

    if st.button("Exportovat jako .txt", type="primary"):
        penset_txt = df_to_penset(edited_df)
        st.download_button("Stáhnout .txt", data=penset_txt, file_name="export.txt", mime="text/plain")
