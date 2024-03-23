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
    get_redirect_url,
    load_error_message,
)

if 'seo_results_df' not in st.session_state or st.session_state['seo_results_df'] is None:
    st.session_state['seo_results_df'] = pd.DataFrame(columns=['URL', 'Redirect URL', 'Status Code', 'Status Crawling', 'Meta Title', 'Meta Description', 'Backlinks to Lifepal'])

st.title("🕷️Backlink Checker")

input_option = st.selectbox("Pilih metode input URL:", ["Text Area", "Upload File CSV"])
if input_option == "Text Area":
    urls = st.text_area("Masukkan URL (pisahkan dengan Enter)", height=200)
    urls = urls.split('\n')
    primary_keyword = "" 
elif input_option == "Upload File CSV":
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])
    if uploaded_file is not None:
        urls_df = pd.read_csv(uploaded_file)
        if "URL" in urls_df.columns:
            urls = urls_df["URL"].tolist()
            primary_keyword = "" 
        else:
            st.warning("File CSV tidak memiliki kolom 'URL'.")
            st.stop()
    else:
        st.warning("Silakan unggah file CSV terlebih dahulu.")
        st.stop()

if st.button("Scrape dan Analisis"):
    result_content = []
    total_urls = len(urls)
    progress_text = "Operation in progress. Please wait."
    progress_bar = st.progress(0, text=progress_text)
    df_placeholder = st.empty()
    
    for index, url in enumerate(urls):
        status_code = get_status_code(url)
        status_code_messages = load_error_message(status_code) 
        final_url = url
        file_html = None
        meta_title = None
        backlinks_lifepal = []
        status = ""
        redirect_url = ""

        try:
            status_code = get_status_code(url)
                    
            if status_code == 301 or status_code == 302:
                redirect_url = get_redirect_url(url)
                final_url = redirect_url
                        
            if status_code == 200 or (status_code == 301 or status_code == 302):
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
                status_code = 500  
        
        data_content_r = {'URL': url, 'Redirect URL': final_url, 'Status Code': status_code, 'Status': status_code_messages, 'Status Crawling': status, }  
        if meta_title:
            data_content_r['Meta Title'] = meta_title
            data_content_r['Meta Description'] = meta_description
            data_content_r['Backlinks to Lifepal'] = backlinks_lifepal
        result_content.append(data_content_r)

        progress_percent = min((index + 1) / total_urls, 1.0) if total_urls != 0 else 1.0
        progress_bar.progress(progress_percent, text=f"Progress: {index+1}/{total_urls} URLs scraped")
        time.sleep(0.1)

        # Update DataFrame dalam session state
        st.session_state['seo_results_df'] = pd.DataFrame(result_content)
        df_placeholder.dataframe(st.session_state['seo_results_df'])

    progress_bar.empty()
