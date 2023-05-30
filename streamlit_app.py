import streamlit as st
import time
from scrape import get_title, get_description, get_content, is_valid_url, get_status_code, domain_disclaimer, get_content_with_html, get_h1, get_headings
from count import count_title_length, count_words, count_meta_description
from element import get_all_headings
from links import get_internal_links
from keywords import check_related_keywords, compare_seo_title_h1, check_primary_keyword_in_h1, check_primary_keyword_in_content



st.title("SEO Content Analysis")
st.write("This app performs an SEO analysis of a website by checking its on-page SEO factors and analyzing its primary and related keywords.")

url_input = st.text_input("Enter a URL", max_chars=500, key="url_input")
url = url_input.strip()
primary_keyword = st.text_input("Enter the primary keywords")
related_keywords = st.text_area("Enter related keywords (separated by newline)")
related_keywords_list = related_keywords.split("\n")

if not url.startswith("http"):
    url = f"https://{url}"

if st.button("Analyze"):
    if not url or not primary_keyword:
        st.warning("Please enter both URL and primary keyword")
    else:
        if not is_valid_url(url):
            st.warning("Please enter a valid URL")
        else:
            if get_status_code(url) != 200:
                st.warning("The website is not up and running")
            else:
                with st.spinner('Scraping the website...'):
                    time.sleep(2)
                    seo_title = get_title(url)
                    h1 = get_h1(url)
                    content_html = get_content_with_html(url)
                    content = get_content(url)
                    headings = get_headings(content_html)
                    title_length = count_title_length(seo_title)
                    meta_description_length = count_meta_description(get_description(url))
                    word_count = count_words(content)
                    related_keywords_result = check_related_keywords(content_html, related_keywords_list)
                    seo_title_h1_result = compare_seo_title_h1(seo_title, h1)
                    keyword_in_h1_result = check_primary_keyword_in_h1(primary_keyword, h1)
                    keyword_density = check_primary_keyword_in_content(primary_keyword, content)

                    seo_title_compatibility_with_h1 = compare_seo_title_h1(seo_title, h1)

                st.header(seo_title)
                st.write(get_description(url))

                # Create table to display primary keyword and results
                st.subheader(":blue[Overview]")
                table_data = {
                    'Item': [
                        "Title Length",
                        'Meta Description Length',
                        'Content Length',
                        'SEO Title Compatibility with H1',
                        'Primary Keyword in H1',
                        'Keyword density'
                    ],
                    'Result': [
                        title_length,
                        meta_description_length,
                        word_count,
                        seo_title_h1_result,
                        keyword_in_h1_result,
                        keyword_density
                    ]
                }
                st.write('\n\n')
                st.table(table_data)

              # Create tabs for different sections
              
                tab1, tab2, tab3= st.tabs(["Headings", "Related Keywords","Internal Links"])
                with tab1:
                        st.subheader(":blue[Headings]")
                        headings = get_all_headings(url)
                        for heading in headings:
                            st.write(heading)
                # Part of the Streamlit main function
                with tab2:
                    st.header(":blue[Related keywords]")
                    st.table(related_keywords_result)
                with tab3:
                    st.subheader(":blue[Internal Links Analysis]")
                    internal_links_table = get_internal_links(url)
                    st.table(internal_links_table)
                             

              
                




