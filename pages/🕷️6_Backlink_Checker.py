import streamlit as st
import pandas as pd
import time
import re
import requests
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
st.title("🕷️Backlink Checker")
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
    total_urls = len(urls)
    progress_text = "Operation in progress. Please wait."
    progress_bar = st.progress(0, text=progress_text)

    for index, url in enumerate(urls):
        status_code = None
        final_url = url  # Inisialisasi final_url dengan url awal
        file_html = None
        meta_title = None
        backlinks_lifepal = []
        status = ""
        redirect_url = ""  # Inisialisasi redirect_url

        try:
    status_code = get_status_code(url)
            
    if status_code == 301 or status_code == 302:
        redirect_url = get_redirect_url(url)
        final_url = redirect_url
                
    if status_code == 200 or (status_code == 301 or status_code == 302):
        # Mengambil final_url setelah penanganan redirection
        file_html = get_html_content(final_url)
        content_text = get_content(final_url, file_html)
        meta_title = get_meta_title(file_html)  
        meta_description = get_meta_description(file_html)

        backlinks = re.findall(r'<a\s+(?:[^>]*?\s+)?href="(https?://(?:www\.)?(?:lifepal\.co\.id|moneysmart\.id)/[^"]*)"', file_html)
        backlinks_lifepal.extend(backlinks) 
        status = "Success"
    else:
        status = "Failed"
    except requests.exceptions.SSLError as e:
        status = "Failed"
        status_code = 500  # Menetapkan status code 500 untuk menunjukkan kesalahan server

        
        data_content_r = {'URL': url, 'Status Code': status_code, 'Status': status, 'Redirect URL': final_url}  # Tambahkan final_url ke data
        if meta_title:
            data_content_r['Meta Title'] = meta_title
            data_content_r['Meta Description'] = meta_description
            data_content_r['Backlinks to Lifepal'] = backlinks_lifepal
        result_content.append(data_content_r)

        # Update progress bar
        progress_percent = min((index + 1) / total_urls, 1.0) if total_urls != 0 else 1.0  # Normalisasi nilai progress_percent
        progress_bar.progress(progress_percent, text=f"Progress: {index+1}/{total_urls} URLs scraped")
        time.sleep(0.1)  # Untuk memberikan sedikit jeda agar progress bar dapat dilihat

    # Hapus progress bar setelah selesai
    progress_bar.empty()
    df_content = pd.DataFrame(result_content)

    # Menyimpan DataFrame ke dalam session state
    st.session_state.seo_df_content = df_content

    # Mencetak DataFrame ke dalam antarmuka pengguna
    st.dataframe(st.session_state.seo_df_content)
