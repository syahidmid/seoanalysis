import streamlit as st
import time
import sys
from scrape import (
    get_title,
    get_description,
    get_content,
    is_valid_url,
    get_status_code,
    domain_disclaimer,
    get_content_with_html,
    get_h1,
    get_headings,
    example_url,
)
from count import count_title_length, count_words, count_meta_description
from element import get_all_headings
from links import get_internal_links
from keywords import (
    check_related_keywords,
    compare_seo_title_h1,
    check_primary_keyword_in_h1,
    check_primary_keyword_in_content,
)

st.title("SEO Content Analysis 🤠")
st.write(
    "This app performs an SEO analysis of a website by checking its on-page SEO factors and analyzing its primary and related keywords."
)

url_input = st.text_input("Enter a URL", max_chars=500, key="url_input")
url = url_input.strip()
primary_keyword = st.text_input("Enter the primary keywords")
with st.expander("Advance"):
    default_related_keywords = "local seo tips\nseo tips and tricks\nwordpress seo tips"
    related_keywords = st.text_area("Enter related keywords (separated by newline)")
    related_keywords_list = related_keywords.split("\n")

if not url.startswith("http"):
    url = f"https://{url}"

if st.button("Analyze"):
    if not url or not primary_keyword:
        st.warning("Please enter both URL and primary keyword")
    elif not is_valid_url(url):
        st.warning("Please enter a valid URL")
    else:
        status_code = get_status_code(url)
        if get_status_code(url) != 200:
            st.warning("The website is not up and running")
            sys.exit(
                1
            )  # Exit the program with an exit code of 1 # Hentikan eksekusi program di sini
        with st.spinner("Start scraping the website..."):
            time.sleep(1)
            seo_title = get_title(url)
            # Lanjutkan eksekusi program di sini
            h1 = get_h1(url)
            st.header(seo_title)
            description = get_description(url)
            st.write(description)

            with st.spinner("Trying to identify the content area..."):
                time.sleep(1)
                disclaimer_message = domain_disclaimer(url)
                st.subheader(":blue[Overview]")
                st.markdown(disclaimer_message)

            with st.spinner("Starting content analysis..."):
                time.sleep(1)
                content_html = get_content_with_html(url)
                content = get_content(url)
                headings = get_headings(content_html)
                title_length = count_title_length(seo_title)

            with st.spinner("Calculating word count..."):
                time.sleep(1)
                word_count = count_words(content)
                meta_description_length = count_meta_description(description)
            with st.spinner("Comparing SEO title with H1..."):
                seo_title_h1_result = compare_seo_title_h1(seo_title, h1)
                keyword_in_h1_result = check_primary_keyword_in_h1(primary_keyword, h1)
            with st.spinner("Calculating keyword density..."):
                time.sleep(1)
                keyword_density = check_primary_keyword_in_content(
                    primary_keyword, content
                )
                related_keywords_result = check_related_keywords(
                    content_html, related_keywords_list
                )

                table_data = {
                    "Item": [
                        "Title Length",
                        "Meta Description Length",
                        "Content Length",
                        "SEO Title Compatibility with H1",
                        "Primary Keyword in H1",
                        "Keyword density",
                    ],
                    "Result": [
                        title_length,
                        meta_description_length,
                        word_count,
                        seo_title_h1_result,
                        keyword_in_h1_result,
                        keyword_density,
                    ],
                }
                st.write("\n\n")
                st.table(table_data)
                outline_expander = st.expander("Outline Analysis")
                related_keywords_expander = st.expander(
                    "Related Keywords", expanded=True
                )
                internal_links_expander = st.expander("Internal Links", expanded=True)

            # Outline Analysis
        with st.expander("Outline", expanded=True):
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                [
                    "My Article",
                    "Competitor 1",
                    "Competitor 2",
                    "Competitor 3",
                    "Competitor 4",
                ]
            )
            with tab1:
                st.subheader(":blue[Headings]")
                headings = get_all_headings(url)
                for heading in headings:
                    st.write(heading)
            # Part of the Streamlit main function
            with tab2:
                st.write("Hello")
            with tab3:
                st.write("Hello")
            with tab4:
                st.write("Hello")
            with tab5:
                st.write("Hello")
        # Related Keywords Analysis
        with st.expander("Related Keywords"):
            st.header(":blue[Related keywords]")

            st.table(related_keywords_result)
        # Internal Links Analysis
        with st.expander("Internal Links"):
            st.subheader(":blue[Internal Links Analysis]")
            internal_links_table = get_internal_links(url)
            st.table(internal_links_table)
