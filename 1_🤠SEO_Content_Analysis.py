import streamlit as st
import time
import sys
import pandas as pd
from urllib.parse import urlparse
from scrapers.scrape import (
    is_valid_url,
    get_status_code,
    domain_disclaimer,
    get_title,
    get_meta_title,
    get_meta_description,
    get_meta_keywords,
    get_canonical_url,
    get_author,
    get_publisher,
    get_language,
    get_content,
    get_content_with_html,
    get_html_content,
    get_h1,
    get_headings,
    get_first_parapraph,
)
from analyzers.links import get_internal_links
from analyzers.count import (
    word_counter,
    character_counter,
)
from analyzers.keywords import (
    compare_seo_title_h1,
    check_related_keywords,
    check_primary_keyword_in_h1,
    check_primary_in_first_p,
    check_primary_keyword_in_content,
    check_primary_keyword_in_headings,
)

st.title("SEO Content Analysis 🤠")
st.write(
    "This app performs an SEO analysis of a website by checking its on-page SEO factors and analyzing its primary and related keywords."
)

url_input = st.text_input(
    "Enter a URL:",
    max_chars=500,
    key="url_input",
    placeholder="https://example.com/seo-strategy/",
)
url = url_input.strip()
parsed_url = urlparse(url)
domain_name = (
    parsed_url.netloc.split(".")[-2]
    if parsed_url.netloc.count(".") >= 2
    else parsed_url.netloc
)
primary_keyword = st.text_input(
    "Enter the primary keywords:", placeholder="best seo strategy"
)
primary_keyword = primary_keyword.lower()
with st.expander("Advance"):
    default_related_keywords = "local seo tips\nseo tips and tricks\nwordpress seo tips"
    related_keywords = st.text_area(
        "Enter related keywords (separated by newline):",
        value="",
        placeholder=default_related_keywords,
    )
    related_keywords_list = [
        keyword.strip() for keyword in related_keywords.split("\n")
    ]
    # URL inputs
    st.write("Enter your competitor SERP")
    url_input1 = st.text_input("URL 1", value="", placeholder="Enter URL 1")
    url_input2 = st.text_input("URL 2", value="", placeholder="Enter URL 2")
    url_input3 = st.text_input("URL 3", value="", placeholder="Enter URL 3")
    url_input4 = st.text_input("URL 4", value="", placeholder="Enter URL 4")

full_report = st.checkbox("See full report.")

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
            html_content = get_html_content(url)
            content_html = get_content_with_html(url)
            content = get_content(url, html_content)
            seo_title = get_title(url)
            meta_description = get_meta_description(html_content)

            st.header(seo_title)
            st.write(meta_description)
            st.write(domain_name)
            with st.spinner("Trying to identify the content area..."):
                time.sleep(1)
                disclaimer_message = domain_disclaimer(url)
                st.subheader(":blue[Overview]")
                st.markdown(disclaimer_message)
                if full_report:
                    st.write("full report")

            with st.spinner("Starting content analysis..."):
                time.sleep(1)
                h1 = get_h1(url)
                headings = get_headings(content_html)
                first_parapraph = get_first_parapraph(html_content)

            with st.spinner("Calculating word count..."):
                time.sleep(1)
                article_length = word_counter(content)
            with st.spinner("Comparing SEO title with H1..."):
                seo_title_h1_result = compare_seo_title_h1(seo_title, h1)
                keyword_in_h1_result = check_primary_keyword_in_h1(primary_keyword, h1)
                keyword_in_headings = check_primary_keyword_in_headings(
                    primary_keyword, headings
                )
                keyword_in_first_paragraph = check_primary_in_first_p(
                    primary_keyword, content
                )
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
                        "Content Length",
                        "SEO Title Compatibility with H1",
                        "Primary Keyword in H1",
                        "Primary Keyword in Headings",
                        "Primary Keyword in First Paragraph",
                        "Keyword density",
                    ],
                    "Result": [
                        article_length,
                        seo_title_h1_result,
                        keyword_in_h1_result,
                        keyword_in_headings,
                        keyword_in_first_paragraph,
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
        with st.expander("Meta Properties", expanded=False):
            meta_title = get_meta_title(html_content)
            meta_keywords = get_meta_keywords(html_content)
            canonical = get_canonical_url(html_content)
            author = get_author(html_content)
            publisher = get_publisher(html_content)
            language = get_language(html_content)

            title_length = character_counter(seo_title)
            meta_description_length = character_counter(meta_description)

            meta_table = {
                "Meta Property": [
                    "Meta Title",
                    "Meta Description",
                    "Keywords",
                    "Canonical",
                    "Author",
                    "Publisher",
                    "Language",
                ],
                "Value": [
                    meta_title,
                    meta_description,
                    meta_keywords,
                    canonical,
                    author,
                    publisher,
                    language,
                ],
                "Analysis Result": [
                    title_length,
                    meta_description_length,
                    "",
                    "",
                    "",
                    "",
                    "",
                ],
            }

            df = pd.DataFrame(meta_table)
            st.table(df)

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
                st.write(h1)
                st.write(url)
                st.write(meta_description)
                for heading in headings:
                    st.write(heading)
            # Part of the Streamlit main function
            with tab2:
                st.write("Hello")
                if url_input1.strip():
                    title_url1 = get_h1(url_input1)
                    description_url1 = get_meta_description(url_input1)
                    content_url1 = get_content_with_html(url_input1)
                    heading_url1 = get_headings(content_url1)
                    st.write(title_url1)
                    st.write(url_input1)
                    st.write(description_url1)
                    if heading_url1:
                        for heading in heading_url1:
                            st.markdown(heading)
                else:
                    st.warning("Please enter URL 1")
            with tab3:
                if url_input2.strip():
                    title_url2 = get_h1(url_input2)
                    description_url2 = get_meta_description(url_input2)
                    content_url2 = get_content_with_html(url_input2)
                    heading_url2 = get_headings(content_url2)
                    st.write(title_url2)
                    st.write(url_input2)
                    st.write(description_url2)
                    if heading_url2:
                        for heading in heading_url2:
                            st.markdown(heading)
                else:
                    st.warning("Please enter URL 1")
            with tab4:
                title_url3 = get_h1(url_input3)
                description_url3 = get_meta_description(url_input3)
                content_url3 = get_content_with_html(url_input3)
                heading_url3 = get_headings(content_url3)
                st.write(title_url3)
                st.write(url_input3)
                st.write(description_url3)
                if heading_url3:
                    for heading in heading_url3:
                        st.markdown(heading)
                else:
                    st.warning("Please enter URL 1")
            with tab5:
                title_url4 = get_h1(url_input4)
                description_url4 = get_meta_description(url_input4)
                content_url4 = get_content_with_html(url_input4)
                heading_url4 = get_headings(content_url4)
                st.write(title_url4)
                st.write(url_input4)
                st.write(description_url4)
                if heading_url4:
                    for heading in heading_url4:
                        st.markdown(heading)
                else:
                    st.warning("Please enter URL 1")
        # Related Keywords Analysis
        with st.expander("Related Keywords"):
            st.header(":blue[Related keywords]")

            st.table(related_keywords_result)
        # Internal Links Analysis
        with st.expander("Internal Links"):
            st.subheader(":blue[Internal Links Analysis]")
            internal_links_table = get_internal_links(url, full_report)
            st.table(internal_links_table)
        # Content
        with st.expander("Content"):
            st.subheader(":blue[Content]")
            st.write(content)
