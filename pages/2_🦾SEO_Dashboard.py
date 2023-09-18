import streamlit as st
import pandas as pd
from scrapers.scrape import (
    is_valid_url,
    get_html_content,
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


# Inisialisasi list data
data = []
if st.button("Scrape dan Analisis"):
    # Inisialisasi list data
    data = []

    # Scraping judul dari setiap URL dan menghitung panjang judul
    for url in urls:
        # Mengambil konten HTML dan judul
        file_html = get_html_content(url)  # Menggunakan fungsi dari scrapers
        meta_title = get_meta_title(file_html)  # Menggunakan fungsi dari scrapers
        meta_description = get_meta_description(file_html)
        meta_title_lenght = word_counter(meta_title)
        meta_desc_lenght = character_counter(meta_description)
        headings = get_headings(file_html)

        entry = {'URL': url, 
        'Meta Title': meta_title,
        'Meta Description': meta_description,
        'Title Lenght': meta_title_lenght,
        'Meta Desc Lenght': meta_desc_lenght}

        # Analisis dengan check_primary_keyword_in_headings jika URL dan primary_keyword ada
        if primary_keyword:
            headings = get_headings(file_html)  # Mengambil headings dari HTML
            keyword_in_headings = check_primary_keyword_in_headings(primary_keyword, headings)
            entry['Keyword di Headings'] = keyword_in_headings  # Simpan hasil analisis dalam entry
        if show_title_length:
            title_len = word_counter(meta_title)
            entry['Panjang Judul'] = title_len
            
        # Menambahkan hasil scraping dan analisis ke list data
        data.append(entry)

    # Membuat dataframe dari data
    df = pd.DataFrame(data)

    # Simpan dataframe ke session state
    st.session_state.seo_results_df = df

# Tampilkan tabel hasil scraping jika ada data
if st.session_state.seo_results_df is not None:
   with st.expander('Content'):
        st.dataframe(st.session_state.seo_results_df)