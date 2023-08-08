import streamlit as st
import urllib
import requests
import pandas as pd
import base64

# Function to call SERP API and get results for a single keyword
def get_serp_results(api_key, query, num=10, lang=None, country=None, device=None):
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "seo-api.p.rapidapi.com",
        "x-user-agent": device,
    }

    query_params = {
        "q": query,
        "num": num,
        "lr": lang,
        "cr": country
    }
    
    resp = requests.get("https://seo-api.p.rapidapi.com/v1/search/" + urllib.parse.urlencode(query_params), headers=headers)
    return resp.json()

# Function to check if URL exists in SERP results and get its position
def check_position(results, url):
    url_slug = url.lower()
    organic_results = results.get("results", [])
    for index, item in enumerate(organic_results, 1):
        item_link = item.get("link", "").lower()
        if url_slug in item_link:
            return index
    return "Not Found"

def get_url(results, url):
    url_slug = url.lower()
    organic_results = results.get("results", [])
    for item in organic_results:
        item_link = item.get("link", "").lower()
        if url_slug in item_link:
            return item_link
    return "Not Found"

# Streamlit app
def main():
    st.title("SERP Checker App")
    api_key = st.text_input("Enter your API key")
    keywords_bulk_text = st.text_area("Enter keywords (one keyword per line)")
    keywords_list = keywords_bulk_text.strip().split("\n")
    
    with st.expander("Settings"):
        url_to_check = st.text_input("Enter URL to check in SERP results", value="lifepal.co.id")
        num_results = st.number_input("Number of results to retrieve (Max: 100)", min_value=1, max_value=100, value=10)
        lang = st.text_input("Language code (e.g., lang_en for English, lang_es for Spanish)", value="ID", max_chars=7)
        country = st.text_input("Country code (e.g., US, CA, DE, AU)", value="ID", max_chars=2)
        device = st.text_input("Device (e.g., mobile, dekstop) ", value="Mobile")
    
    results_df = pd.DataFrame(columns=["Keyword", "Position", "URL"])
   
    # Button to start the search
    if st.button("Start Search"):
        with st.spinner("Searching..."):
            for keyword in keywords_list:
                # Call SERP API for each keyword
                results = get_serp_results(api_key, keyword, num=num_results, lang=lang, country=country, device=device)
                position = check_position(results, url_to_check)
                original_url = get_url(results, url_to_check)
                
                # Append the result to the DataFrame
                results_df = results_df.append({"Keyword": keyword, "Position": position, "URL": original_url}, ignore_index=True)
            
            # Display the results in a table
            st.write("SERP Results:")
            st.dataframe(results_df)
            
            # Show balloons when the search is completed
            st.balloons()

    # Download CSV button
    if not results_df.empty and st.button("Download CSV"):
        csv_data = results_df.to_csv(index=False)
        b64 = base64.b64encode(csv_data.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="serp_results.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


