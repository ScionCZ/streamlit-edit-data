import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Pen set editor", layout="wide")

# Funkce na parsování pen set souboru
def parse_penset(txt):
    lines = txt.strip().split('\n')
    data_lines = []
    start = False
    for line in lines:
        if line.startswith("Index"):
            start = True
            continue
        if start:
            if line.strip() == '' or line.startswith('*****'):
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
                    'Tloušťka (v mm)': float(parts[4]),
                    'Používá se': parts[5],
                    'Popis': parts[6]
                })
            except ValueError:
                continue
    return pd.DataFrame(rows)

# Funkce na vytvoření barevného hex kódu
def rgb_to_hex(r, g, b):
    return '#{:02X}{:02X}{:02X}'.format(r, g, b)

# Titulek a upload
st.title("Pen set editor")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)

    # Přidání náhledového sloupce
    df["Náhled"] = df.apply(lambda row: f'<div style="width: 100%%; height: 20px; background-color: {rgb_to_hex(row["Červená"], row["Zelená"], row["Modrá"])}"></div>', axis=1)

    # Umožnění editace vybraných sloupců (kromě Index a Používá se)
    editable_cols = ['Červená', 'Zelená', 'Modrá', 'Tloušťka (v mm)', 'Popis']
    edited_df = st.data_editor(
        df,
        column_config={
            "Náhled": st.column_config.Column("Náhled", help="Barevný náhled", disabled=True, html=True),
            "Index": st.column_config.Column("Index", disabled=True),
            "Používá se": st.column_config.Column("Používá se", disabled=True)
        },
        disabled=[col for col in df.columns if col not in editable_cols],
        use_container_width=True,
        height=600,
        num_rows="dynamic"
    )

    # Export tlačítko
    if st.button("Exportovat upravený pen set", type="primary"):
        output = io.StringIO()
        output.write("---- PERA (2-TLČ) ----\n")
        output.write("Index\tČervená\tZelená\tModrá\tTloušťka (v mm)\tPoužívá se\tPopis\n")
        output.write("*****\t*****\t*****\t*****\t*****\t*****\t*****\n")
        for _, row in edited_df.iterrows():
            output.write(f"{row['Index']}\t{int(row['Červená'])}\t{int(row['Zelená'])}\t{int(row['Modrá'])}\t{row['Tloušťka (v mm)']:.6f}\t{row['Používá se']}\t{row['Popis']}\n")
        st.download_button("Stáhnout .txt soubor", output.getvalue(), file_name="upraveny_pen_set.txt")
