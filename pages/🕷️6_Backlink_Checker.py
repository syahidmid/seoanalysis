import streamlit as st
import pandas as pd
import time
import re
import requests
from scrapers.scrape import (
    get_status_code,
    get_html_content,
    get_meta_title,
    get_meta_description,
    get_redirect_url,
)

# Initialize DataFrame
if 'seo_results_df' not in st.session_state or st.session_state['seo_results_df'] is None:
    st.session_state['seo_results_df'] = pd.DataFrame(columns=['URL', 'Redirect URL', 'Status Code', 'Status Crawling', 'Meta Title', 'Meta Description', 'Backlinks Custom'])

st.title("🕷️Backlink Checker")
urls = st.text_area("Masukkan URL (pisahkan dengan Enter)", height=200, key="url_input").split('\n')
target_url1 = st.text_input("Masukkan Target URL 1:", 'lifepal.co.id', key="target_url_1")
target_url2 = st.text_input("Masukkan Target URL 2:", 'moneysmart.id', key="target_url_2")

if st.button("Scrape dan Analisis", key="analyze_button"):
    result_content = []
    total_urls = len(urls)
    progress_bar = st.progress(0)
    df_placeholder = st.empty()

    for index, url in enumerate(urls):
        status_code = get_status_code(url)
        final_url = url
        meta_title = None 
        meta_description = None 
        backlinks_custom = []

        try:
            if status_code in [301, 302]:
                redirect_url = get_redirect_url(url)
                final_url = redirect_url
            
            if status_code == 200 or status_code in [301, 302]:
                file_html = get_html_content(final_url)
                meta_title = get_meta_title(file_html)
                meta_description = get_meta_description(file_html)
                
                # Dynamic regex pattern based on user input
                regex_pattern = fr'<a\s+(?:[^>]*?\s+)?href="(https?://(?:www\.)?({re.escape(target_url1)}|{re.escape(target_url2)})/[^"]*)"'
                backlinks = re.findall(regex_pattern, file_html)
                backlinks_custom.extend(backlinks)

                status = "Success"
            else:
                status = "Failed"
        except requests.exceptions.RequestException:
            status = "Failed"
            status_code = 500

        # Add result to DataFrame
        data_row = {
            'URL': url,
            'Redirect URL': final_url,
            'Status Code': status_code,
            'Status Crawling': status,
            'Meta Title': meta_title,
            'Meta Description': meta_description,
            'Backlinks Custom': backlinks_custom
        }
        result_content.append(data_row)

        # Update progress bar
        progress_bar.progress((index + 1) / total_urls)
        time.sleep(0.1)

    # Update DataFrame in session state and display
    st.session_state['seo_results_df'] = pd.DataFrame(result_content)
    df_placeholder.dataframe(st.session_state['seo_results_df'])

    progress_bar.empty()
