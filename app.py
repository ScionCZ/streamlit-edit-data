import streamlit as st
import pandas as pd
import io

# Funkce na parsování .txt souboru se strukturou pen setu
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
                continue  # přeskočí řádky s nevalidními daty

    df = pd.DataFrame(rows)
    df['Barva'] = df.apply(lambda row: f"background-color: rgb({row['Červená']}, {row['Zelená']}, {row['Modrá']})", axis=1)
    return df

st.set_page_config(page_title="Pen set editor", layout="wide")
st.title("Pen set editor")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)

    # Rozdělení na editovatelné a needitovatelné sloupce
    editable_cols = ['Červená', 'Zelená', 'Modrá', 'Tloušťka (v mm)', 'Popis']
    readonly_cols = ['Index', 'Používá se']

    st.write("### Upravitelná tabulka")
    styled_df = df[[*readonly_cols, *editable_cols]].copy()

    # Přidání náhledu barvy vpravo od Modrá
    styled_df.insert(4, 'Náhled barvy', [''] * len(df))
    for i in styled_df.index:
        r, g, b = styled_df.loc[i, 'Červená'], styled_df.loc[i, 'Zelená'], styled_df.loc[i, 'Modrá']
        styled_df.at[i, 'Náhled barvy'] = f"\
            <div style='width: 40px; height: 20px; background-color: rgb({r},{g},{b}); border: 1px solid #000;'></div>"

    # Použití Streamlit AgGrid pro editaci a zobrazení HTML stylu
    from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
    gb = GridOptionsBuilder.from_dataframe(styled_df)
    gb.configure_columns(editable_cols, editable=True)
    gb.configure_column("Náhled barvy", cellRenderer=JsCode('''
        function(params) {
            return params.value;
        }
    '''), editable=False, wrapText=True, autoHeight=True)

    gridOptions = gb.build()
    response = AgGrid(
        styled_df,
        gridOptions=gridOptions,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        height=500,
        reload_data=True
    )

    updated_df = response['data']

    # Přidat tlačítko pro export
    st.write("### Exportovat")
    if st.button("Exportovat jako .txt", type="primary"):
        export_df = updated_df[["Index", "Červená", "Zelená", "Modrá", "Tloušťka (v mm)", "Používá se", "Popis"]]
        export_txt = 'Index\tČervená\tZelená\tModrá\tTloušťka (v mm)\tPoužívá se\tPopis\n'
        for _, row in export_df.iterrows():
            export_txt += f"{row['Index']}\t{row['Červená']}\t{row['Zelená']}\t{row['Modrá']}\t{row['Tloušťka (v mm)']:.6f}\t{row['Používá se']}\t{row['Popis']}\n"

        st.download_button(
            label="Stáhnout .txt soubor",
            data=export_txt,
            file_name="upraveny_penset.txt",
            mime="text/plain"
        )
