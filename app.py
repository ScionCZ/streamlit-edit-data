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
            if not line.strip() or line.startswith("*****"):
                continue
            parts = line.strip().split('\t')
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

def generate_txt(df):
    header = "---- PERA (2-TL\u010c) ----\nIndex\t\u010cerven\u00e1\tZelen\u00e1\tModr\u00e1\tTlou\u0161\u0165ka (v mm)\tPou\u017e\u00edv\u00e1 se\tPopis\n*****\t*****\t*****\t*****\t*****\t*****\t*****"
    lines = [
        f"{row['Index']}\t{row['\u010cerven\u00e1']}\t{row['Zelen\u00e1']}\t{row['Modr\u00e1']}\t{row['Tlou\u0161\u0165ka (v mm)']:.6f}\t{row['Pou\u017e\u00edv\u00e1 se']}\t{row['Popis']}"
        for _, row in df.iterrows()
    ]
    return header + "\n" + "\n".join(lines)

st.title("Pen set editor")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    rows = []
    df = parse_penset(content)

    st.subheader("Edituj tabulku")
    edited_df = st.data_editor(df, num_rows="dynamic")

    st.subheader("Color Picker náhled")
    for i in range(len(edited_df)):
        r, g, b = edited_df.loc[i, 'Červená'], edited_df.loc[i, 'Zelená'], edited_df.loc[i, 'Modrá']
        color_hex = '#%02x%02x%02x' % (r, g, b)
        picked_color = st.color_picker(f"Barva pro Index {edited_df.loc[i, 'Index']}", color_hex, key=f"picker_{i}")
        # Update RGB zpět do DataFrame
        picked_color_rgb = tuple(int(picked_color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
        edited_df.at[i, 'Červená'] = picked_color_rgb[0]
        edited_df.at[i, 'Zelená'] = picked_color_rgb[1]
        edited_df.at[i, 'Modrá'] = picked_color_rgb[2]

    st.subheader("Export dat")
    if st.button("💾 Exportovat jako TXT", type="primary"):
        result_txt = generate_txt(edited_df)
        st.download_button(
            label="📥 Stáhnout .txt",
            data=result_txt,
            file_name="exported_penset.txt",
            mime="text/plain"
        )
