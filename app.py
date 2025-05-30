import streamlit as st
import pandas as pd


def parse_penset(txt):
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

    rows = []
    for line in data_lines:
        parts = line.split('\t')
        if len(parts) >= 7:
            rows.append({
                'Index': parts[0],
                'Červená': int(parts[1]),
                'Zelená': int(parts[2]),
                'Modrá': int(parts[3]),
                'Tloušťka (v mm)': parts[4],
                'Používá se': parts[5],
                'Popis': parts[6]
            })
    return pd.DataFrame(rows)


# Stylování tlačítek
st.markdown("""
<style>
div.stDownloadButton > button:first-child {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}
div.stButton > button:first-child {
    background-color: #2196F3;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("Pen set editor")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)

    st.write("Načtená data:")
    edited_df = st.data_editor(df, num_rows="dynamic")

    # Výběr barvy pro záznam
    st.write("\n### Vyber barvu pro náhled")
    barva = st.color_picker("Zvol barvu", value="#000000")
    st.write(f"Vybral jsi: {barva}")

    # Export
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Stáhni upravená data jako CSV",
        data=csv,
        file_name='upraveny_pen_set.csv',
        mime='text/csv',
    )
