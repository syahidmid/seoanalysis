import streamlit as st
import pandas as pd
import re
from scrapers.scrape import (
    is_valid_url,
    get_status_code,
    get_html_content,
    get_content,
    get_meta_title,
    get_meta_description,
    get_headings,
)
from analyzers.keywords import (
    compare_seo_title_h1,
    check_related_keywords,
    check_primary_keyword_in_h1,
    check_primary_in_first_p,
    check_primary_keyword_in_content,
    check_primary_keyword_in_headings,
)
from analyzers.count import (
    word_counter,
    character_counter,
)
# Initialize session state
if 'seo_results_df' not in st.session_state:
    st.session_state['seo_results_df'] = None

# Judul aplikasi
st.title("Bulk Audit")
# Pengaturan
with st.expander("Pengaturan"):
    show_title_length = st.checkbox("Tampilkan Panjang Judul")

# Pilihan input URL
input_option = st.selectbox("Pilih metode input URL:", ["Text Area", "Upload File CSV", "URL dan Kata Kunci"])
if input_option == "Text Area":
    # Input URL dari pengguna melalui text area
    urls = st.text_area("Masukkan URL (pisahkan dengan Enter)", height=200)
    urls = urls.split('\n')
    primary_keyword = ""  # Kosongkan primary_keyword
elif input_option == "Upload File CSV":
    # Unggah file CSV
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])
    if uploaded_file is not None:
        urls_df = pd.read_csv(uploaded_file)
        # Periksa apakah kolom "URL" ada dalam DataFrame
        if "URL" in urls_df.columns:
            urls = urls_df["URL"].tolist()
            primary_keyword = ""  # Kosongkan primary_keyword
        else:
            st.warning("File CSV tidak memiliki kolom 'URL'.")
            st.stop()
    else:
        st.warning("Silakan unggah file CSV terlebih dahulu.")
        st.stop()
else:
    # Input URL dan Kata Kunci dari pengguna
    primary_keyword = ""
    uploaded_file = st.file_uploader("Unggah file CSV (harus berisi dua kolom: URL, Primary Keyword)", type=["csv"])
    if uploaded_file is not None:
        urls_df = pd.read_csv(uploaded_file)
        
        # Simpan nama kolom dalam bentuk array
        column_names = urls_df.columns.tolist()

        # Periksa apakah kolom "URL" dan "Primary Keyword" ada dalam DataFrame
        if "URL" in column_names and "Primary Keyword" in column_names:
            urls = urls_df["URL"].tolist()
            primary_keywords = urls_df["Primary Keyword"].tolist()
        else:
            st.warning("File CSV harus memiliki dua kolom: URL dan Primary Keyword.")
            st.stop()
    else:
        st.warning("Silakan unggah file CSV terlebih dahulu.")
        st.stop()

if st.button("Scrape dan Analisis"):
    result_content = []

    for url in urls:
        status_code = get_status_code(url)
        file_html = None
        meta_title = None
        backlinks_lifepal = []
        if status_code == 200:
            file_html = get_html_content(url)
            content_text = get_content(url,file_html)
            meta_title = get_meta_title(file_html)  
            meta_description = get_meta_description(file_html)

            backlinks = re.findall(r'(?<=<a\s+(?:[^>]*?\s+)?href=")(https?:\/\/(?:www\.)?lifepal\.co\.id\/[^"]*)(?=")', content_text)
            backlinks_lifepal.extend(backlinks) 
           
        data_content_r = {'URL': url, 'Status Code': status_code}
        if meta_title:
            data_content_r['Meta Title'] = meta_title
            data_content_r['Meta Description'] = meta_description
            data_content_r['Backlinks to Lifepal'] = backlinks_lifepal
        result_content.append(data_content_r)

    df_content = pd.DataFrame(result_content)
    st.session_state.seo_df_content = df_content
    if st.session_state.seo_df_content is not None:
        st.dataframe(st.session_state.seo_df_content)
        

