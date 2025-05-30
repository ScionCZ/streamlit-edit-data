import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Pen Set Editor", layout="wide")

# Funkce na parsování .txt souboru s pen setem
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
            parts = line.split('\t')
            if len(parts) >= 7:
                try:
                    data_lines.append({
                        'Index': int(parts[0]),
                        'Červená': int(parts[1]),
                        'Zelená': int(parts[2]),
                        'Modrá': int(parts[3]),
                        'Tloušťka (v mm)': float(parts[4]),
                        'Používá se': parts[5],
                        'Popis': parts[6]
                    })
                except ValueError:
                    continue  # Přeskočí řádek pokud čísla nejsou validní

    return pd.DataFrame(data_lines)

# Funkce na konverzi dataframe zpět do formátu .txt
def export_to_txt(df):
    output = io.StringIO()
    output.write("---- PERA (2-TLČ) ----\n")
    output.write("Index\tČervená\tZelená\tModrá\tTloušťka (v mm)\tPoužívá se\tPopis\n")
    output.write("*****\t*****\t*****\t*****\t*****\t*****\t*****\n")
    for _, row in df.iterrows():
        line = f"{row['Index']}\t{row['Červená']}\t{row['Zelená']}\t{row['Modrá']}\t{row['Tloušťka (v mm)']:.6f}\t{row['Používá se']}\t{row['Popis']}\n"
        output.write(line)
    return output.getvalue()

# Hlavní aplikace
st.title("🖊️ Pen Set Editor")

uploaded_file = st.file_uploader("Nahraj .txt soubor s pen setem", type=["txt"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = parse_penset(content)

    st.success("Soubor úspěšně načten!")
    st.markdown("### Edituj data")
    edited_df = st.data_editor(df, num_rows="dynamic")

    # Color picker (volitelný)
    st.markdown("### 🎨 Color Picker pro testování")
    selected_color = st.color_picker("Vyber barvu", value="#000000")

    # Export tlačítko
    st.markdown("### 📤 Export")
    export_txt = export_to_txt(edited_df)
    st.download_button("💾 Exportuj jako .txt", data=export_txt, file_name="exported_pen_set.txt", mime="text/plain", use_container_width=True)

    # Debug info
    st.markdown(f"Aktuální vybraná barva: `{selected_color}`")
