import streamlit as st
import pandas as pd
import io

st.set_page_config(layout="wide")


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


def dataframe_with_color_preview(df):
    df = df.copy()
    df["Barva náhled"] = df.apply(
        lambda row: f"<div style='width:20px;height:20px;background-color:rgb({row['Červená']},{row['Zelená']},{row['Modrá']});border-radius:4px'></div>",
        axis=1,
    )
    return df


st.title("Pen set editor s barvou")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)

    # Náhled barev
    df_viz = dataframe_with_color_preview(df)

    # Zobrazení s HTML renderem barvy
    st.markdown("### Náhled dat s barvami")
    st.write(
        df_viz.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

    # Export
    if st.button("Exportovat jako .txt", type="primary"):
        output = io.StringIO()
        output.write("Index\tČervená\tZelená\tModrá\tTloušťka (v mm)\tPoužívá se\tPopis\n")
        for _, row in df.iterrows():
            output.write(
                f"{row['Index']}\t{row['Červená']}\t{row['Zelená']}\t{row['Modrá']}\t{row['Tloušťka (v mm)']:.6f}\t{row['Používá se']}\t{row['Popis']}\n"
            )
        st.download_button("Stáhnout upravený soubor", output.getvalue(), file_name="upraveny_penset.txt")
