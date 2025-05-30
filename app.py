import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Pen Set Editor", layout="wide")

# Funkce pro parsování pen setu
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
                'Tloušťka (v mm)': float(parts[4]),
                'Používá se': parts[5],
                'Popis': parts[6]
            })
    df = pd.DataFrame(rows)
    return df

# Funkce pro vytvoření barevného sloupce
def add_color_preview(df):
    df['Barva'] = df.apply(lambda row: f"""
        <div style='width: 30px; height: 20px; background-color: rgb({row['Červená']}, {row['Zelená']}, {row['Modrá']}); border: 1px solid #000;'></div>""", axis=1)
    return df

st.title("Pen set editor")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)
    df = add_color_preview(df)

    # Zobrazit tabulku s HTML náhledy barev
    st.markdown("### Náhled dat")
    st.write("Edituj tabulku kromě sloupců Index a Používá se:")

    # Připravit editovatelný DataFrame (bez Index a Používá se)
    editable_df = df.drop(columns=["Index", "Používá se", "Barva"])
    edited_df = st.data_editor(editable_df, use_container_width=True, num_rows="dynamic", hide_index=True)

    # Aktualizovat původní df editovanými daty
    df.update(edited_df)
    df = add_color_preview(df)  # Reaplikace barev po změně RGB

    # Sloučit zpět pro zobrazení
    display_df = df[["Index", "Červená", "Zelená", "Modrá", "Barva", "Tloušťka (v mm)", "Používá se", "Popis"]]

    # Zobrazit jako HTML tabulku s barvami
    st.markdown("### Upravená data s barevným náhledem")
    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Export tlačítko
    if st.button("Exportovat jako CSV", type="primary"):
        csv = df.drop(columns=["Barva"]).to_csv(index=False).encode("utf-8")
        st.download_button("Stáhnout CSV", csv, "upraveny_pen_set.csv", "text/csv", key="download-csv")
