import streamlit as st
import pandas as pd
from scrapers.scrape import (
    is_valid_url,
    get_status_code,
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

if st.button("Scrape dan Analisis"):
    # Inisialisasi dua list data
    result_content = []
    result_internal_links = []

    # Scraping judul dari setiap URL dan menghitung panjang judul
    for url in urls:
        # Mengecek status code situs web
        status_code = get_status_code(url)

        # Mengambil konten HTML dan judul jika status code adalah 200
        file_html = None
        meta_title = None
        if status_code == 200:
            file_html = get_html_content(url)  # Menggunakan fungsi dari scrapers
            meta_title = get_meta_title(file_html)  # Menggunakan fungsi dari scrapers
            meta_description = get_meta_description(file_html)
            meta_title_length = word_counter(meta_title)
            meta_desc_length = character_counter(meta_description)
            headings = get_headings(file_html)

        # Buat entri untuk URL dan Status Code (dan Judul jika status code adalah 200)
        data_content_r = {'URL': url, 'Status Code': status_code}
        if meta_title:
            data_content_r['Meta Title'] = meta_title
            data_content_r['Meta Description'] = meta_description
            data_content_r['Title Length'] = meta_title_length
            data_content_r['Meta Desc Length'] = meta_desc_length

        # Analisis dengan check_primary_keyword_in_headings jika URL dan primary_keyword ada
        if primary_keyword and status_code == 200:
            headings = get_headings(file_html)  # Mengambil headings dari HTML
            keyword_in_headings = check_primary_keyword_in_headings(primary_keyword, headings)
            data_content_r['Keyword di Headings'] = keyword_in_headings  # Simpan hasil analisis dalam entry

        # Menambahkan hasil scraping dan analisis ke list data
        result_content.append(data_content_r)

    # Membuat dataframe dari data
    df_content = pd.DataFrame(result_content)

    # Simpan dataframe ke session state
    st.session_state.seo_df_content = df_content

    # Tampilkan tabel hasil scraping jika ada data
    if st.session_state.seo_df_content is not None:
        with st.expander('Content'):
            st.dataframe(st.session_state.seo_df_content)
        
    # --- Proses Scraping Data Internal Links ---

    # ... (sama seperti proses scraping konten, hanya berbeda jenis data)

    # Menambahkan hasil scraping data internal links ke list data
    # (gunakan result_internal_links dan data_internal_links_r seperti sebelumnya)

    # Membuat dataframe dari data internal links
    df_links = pd.DataFrame(result_internal_links)

    # Simpan dataframe data internal links ke session state
    st.session_state.seo_df_links = df_links

    # Tampilkan tabel hasil scraping data internal links jika ada data
    if st.session_state.seo_df_links is not None:
        with st.expander('Internal Links'):
            st.dataframe(st.session_state.seo_df_links)
