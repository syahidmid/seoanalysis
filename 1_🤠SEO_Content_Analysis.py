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
from analyzers.links import (
    get_internal_links, 
    utm_cleaner, 
    link_contains_hash, 
    find_duplicate_links,
    count_internal_links,
    internal_link_density,
)
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
st.set_page_config(
    page_title="SEO Content Analysis",
    page_icon="👋",
    layout= "wide",
    initial_sidebar_state="auto",
)
# Initialize session state
if 'results' not in st.session_state:
    st.session_state['results'] = {}

st.title("SEO Content Analysisssss 🤠 >")
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
            )  
        with st.spinner("Start scraping the website..."):
            time.sleep(1)
            domain_name = domain_name
            file_html = get_html_content(url)
            content_text = get_content(url, file_html)
            content_html = get_content_with_html(url, file_html)
            meta_title = get_meta_title(file_html)
            meta_description = get_meta_description(file_html)
            meta_keywords = get_meta_keywords(file_html)
            disclaimer_message = domain_disclaimer(url)
            canonical = get_canonical_url(file_html)
            author = get_author(file_html)
            publisher = get_publisher(file_html)
            language = get_language(file_html)
            h1 = get_h1(file_html)
            headings = get_headings(content_html)
            first_parapraph = get_first_parapraph(content_html)

            internal_links_data = get_internal_links(url, content_html)
            internal_links_total = count_internal_links(url, content_html)
            
            # Membuat daftar status_code dengan status kode untuk setiap URL di internal_links_data
            
            


            data_internal_links = []
            # Iterasi melalui internal links dan anchor text
            for link, anchor_text in internal_links_data:
                cleaned_link = utm_cleaner(link)
                if not link_contains_hash(cleaned_link):
                    entry = {
                        "Link": cleaned_link,
                        "Anchor Text": anchor_text
                    }
                    data_internal_links.append(entry)

            data_internal_links_with_status = []
            # Iterasi melalui internal links dan anchor text
            for link, anchor_text in internal_links_data:
                status_code = get_status_code(link)
                cleaned_link = utm_cleaner(link)
                if not link_contains_hash(cleaned_link):
                    entry = {
                        "Link": cleaned_link,
                        "Anchor Text": anchor_text,
                        "Status Code": status_code
                    }
                    data_internal_links_with_status.append(entry)
           

            if full_report:
                # Jika full report, gabungkan data_internal_links dengan status_codes
                internal_links_table = pd.DataFrame(data_internal_links_with_status)
            
            else:
                # Jika tidak full report, cukup gunakan data_internal_links
                internal_links_table = pd.DataFrame(data_internal_links)
            
            duplicate_links = find_duplicate_links(internal_links_data)
                            

           
        with st.spinner("Starting content analysis..."):
            time.sleep(1)
            article_length = word_counter(content_text)
            title_length = character_counter(meta_title)
            meta_description_length = character_counter(meta_description)
            seo_title_in_h1 = compare_seo_title_h1(meta_title, h1)
            keyword_in_h1 = check_primary_keyword_in_h1(primary_keyword, h1)
            keyword_in_headings = check_primary_keyword_in_headings(primary_keyword, headings)
            keyword_in_first_paragraph = check_primary_in_first_p(primary_keyword, content_text)
            keyword_density = check_primary_keyword_in_content(primary_keyword, content_text)
            related_keywords = check_related_keywords(content_text, related_keywords_list)
            link_density = internal_link_density(internal_links_total, article_length)

        with st.spinner("Starting competitors analysis..."):
            

            warning_message = ""
            table_data_competitor1 = ""
            if url_input1.strip():
                file_html = get_html_content(url_input1)
                title_url = get_h1(file_html)
                table_data_competitor1 = {
                    "Item": [
                        "Title",
                    ],
                    "Result": [
                        title_url,
                    ],
                }
            else:
                warning_message = "Please enter URL"
            table_data_competitor2 = ""
            if url_input2.strip():
                file_html = get_html_content(url_input2)
                title_url = get_h1(file_html)
                table_data_competitor2 = {
                    "Item": [
                        "Title",
                    ],
                    "Result": [
                        title_url,
                    ],
                }
            else:
                warning_message = "Please enter URL"
            
            table_data_competitor3 = ""
            if url_input3.strip():
                file_html = get_html_content(url_input3)
                title_url = get_h1(file_html)
                table_data_competitor3 = {
                    "Item": [
                        "Title",
                    ],
                    "Result": [
                        title_url,
                    ],
                }
            else:
                warning_message = "Please enter URL"
           
            table_data_competitor4 = ""
            if url_input4.strip():
                file_html = get_html_content(url_input4)
                title_url = get_h1(file_html)
                table_data_competitor4 = {
                    "Item": [
                        "Title",
                    ],
                    "Result": [
                        title_url,
                    ],
                }
            else:
                warning_message = "Please enter URL"
            
        with st.spinner("Presenting the analysis results...."):
            time.sleep(1)
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
                        seo_title_in_h1,
                        keyword_in_h1,
                        keyword_in_headings,
                        keyword_in_first_paragraph,
                        keyword_density,
                    ],
                }
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
            
        # Save results to session state
        st.session_state['results']['h1'] = h1
        st.session_state['results']['url'] = url
        st.session_state['results']['file_html'] = file_html
        st.session_state['results']['content_text'] = content_text
        st.session_state['results']['headings'] = headings
        st.session_state['results']['table_data'] = table_data
        st.session_state['results']['meta_table'] = meta_table
        st.session_state['results']['domain_name'] = domain_name
        st.session_state['results']['meta_description'] = meta_description
        st.session_state['results']['disclaimer_message'] = disclaimer_message
        st.session_state['results']['related_keywords'] = related_keywords
        st.session_state['results']['internal_links_table'] = internal_links_table
        st.session_state['results']['internal_links_data'] = internal_links_data
        st.session_state['results']['internal_links_total'] = internal_links_total
        st.session_state['results']['duplicate_links'] = duplicate_links
        st.session_state['results']['link_density'] = link_density
        st.session_state['results']['url_input1'] = url_input1
        st.session_state['results']['url_input2'] = url_input2
        st.session_state['results']['url_input3'] = url_input3
        st.session_state['results']['url_input4'] = url_input4
        st.session_state['results']['table_competitor1'] = table_data_competitor1
        st.session_state['results']['table_competitor2'] = table_data_competitor2
        st.session_state['results']['table_competitor3'] = table_data_competitor3
        st.session_state['results']['table_competitor4'] = table_data_competitor4
        st.session_state['results']['warning_message'] = warning_message

# Display results using session state
if 'results' in st.session_state:
    results = st.session_state['results']
    if 'h1' in results:
        h1 = results['h1']
        meta_description = results.get('meta_description')
        domain_name = results.get('domain_name')
        disclaimer_message = results.get('disclaimer_message')
        url = results.get('url')
        table_data = results.get('table_data')
        related_keywords_result = results.get('related_keywords')
        internal_links_table = results.get('internal_links_table')
        internal_links_data = results.get('internal_links_data')
        internal_links_total = results.get('internal_links_total')
        link_density = results.get('link_density')
        duplicate_links = results.get('duplicate_links')
        meta_table = results.get('meta_table')
        content_html = results.get('content_html')
        content_text = results.get('content_text')
        file_html = results.get('file_html')
        url_input1 = results.get('url_input1')
        url_input2 = results.get('url_input2')
        url_input3 = results.get('url_input3')
        url_input4 = results.get('url_input4')
        table_data_competitor1 = results.get('table_competitor1')
        table_data_competitor2 = results.get('table_competitor2')
        table_data_competitor3 = results.get('table_competitor3')
        table_data_competitor4 = results.get('table_competitor4')
        warning_message = results.get('warning_message')

        st.header(h1)
        st.write(meta_description)
        st.write(domain_name)
        st.subheader(":blue[Overview]")
        st.write(disclaimer_message)
        st.write("\n\n")
        st.table(table_data)

        with st.expander("Meta Properties", expanded=False):
            st.table(meta_table)

        with st.expander("Outline", expanded=False):
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
                if 'headings' in results:
                    headings = results['headings']
                    for heading in headings:
                        st.write(heading)

            with tab2:
                st.write("Hello")
                if table_data_competitor1:
                    st.table(table_data_competitor1)
                else:
                    st.warning(warning_message)
            with tab3:
                st.write("Hello")
                if table_data_competitor2:
                    st.table(table_data_competitor2)
                else:
                    st.warning(warning_message)
            with tab4:
                if table_data_competitor3:
                    st.table(table_data_competitor3)
                else:
                    st.warning(warning_message)
            with tab5:
                if table_data_competitor4:
                    st.table(table_data_competitor4)
                else:
                    st.warning(warning_message)

        # Related Keywords Analysis
        with st.expander("Related Keywords"):
            st.header(":blue[Related keywords]")
            st.table(related_keywords_result)
        # Internal Links Analysis
        with st.expander("Internal Links"):
            st.subheader(":blue[Internal Links Analysis]")
            # Menampilkan informasi kepada pengguna
            """
            ✂️ We present data that has been cleaned using `utm_cleaner()` and exclude `link_contains_hash()`. But don't worry, we have executed the `status_code()` on all original URLs.
            """ 
            
            st.write(f"Total Inlinks = {internal_links_total} ({link_density:.2f}% of the total words)")
           
            if duplicate_links:
                for link in duplicate_links:
                    count = internal_links_data.count(link)
                    st.write(f"❌ Found {count} duplicate internal link")
            else:
                st.write("✅ There are no duplicate links in the list of links.")
            st.table(internal_links_table)
        # Content Text
        with st.expander("Content"):
            st.subheader(":blue[Content]")
            st.write(content_text)
       
      