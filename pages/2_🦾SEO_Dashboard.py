import streamlit as st
import pandas as pd
import os
import shutil
import numpy as np


st.title("SEO Dashboard")

# Create the new directory if it doesn't exist
folder_path = "./new report"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Initialize all_data and media_o as empty dataframes
all_data = pd.DataFrame()
media_o = pd.DataFrame()

# Create a sidebar for file upload
uploaded_file = st.file_uploader("Choose a file", key="1")

if uploaded_file is not None:
    # Get the file name
    file_name = uploaded_file.name

    # Save the uploaded file to the new directory
    with open(os.path.join(folder_path, file_name), "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read the media o file from the new directory
    media_o = pd.read_csv(os.path.join(folder_path, file_name))

    # Check if 'URL' and 'Keyword' columns are in the dataframe
    if "URL" not in media_o.columns or "Keyword" not in media_o.columns:
        st.write("Error: Columns 'URL' and/or 'Keyword' not found in the dataframe.")
    else:
        # Create new column
        media_o["search_key"] = media_o["URL"] + " | " + media_o["Keyword"]

        # Add new columns
        media_o["Current Position"] = ""
        media_o["Keyword found in SERPRobot"] = ""

        # Save to a new CSV file in the new directory
        new_file_path = os.path.join(folder_path, "Media O.csv")
        media_o.to_csv(new_file_path, index=False)

        # Display the dataframe as a table in the Streamlit app
        items_per_page = 10
        n_pages = len(media_o) // items_per_page
        if len(media_o) % items_per_page > 0:
            n_pages += 1
        page_number = st.number_input(
            label="Page Number", min_value=1, max_value=n_pages, step=1
        )
        start_index = items_per_page * (page_number - 1)
        end_index = start_index + items_per_page

        # Display the dataframe as a table in the Streamlit app
        st.dataframe(
            media_o[start_index:end_index].style.set_properties(
                **{"text-align": "left"}
            )
        )

        # Create a download button for the new file
        with open(new_file_path, "rb") as f:
            bytes_data = f.read()
        st.download_button(
            label="Download Media O.csv",
            data=bytes_data,
            file_name="Media O.csv",
            mime="text/csv",
        )


# Create a sidebar for multiple file upload
with st.expander("Upload SERP Robot"):
    uploaded_files = st.file_uploader(
        "Choose files", accept_multiple_files=True, key="2"
    )

    if uploaded_files:
        # Get the file names
        file_names = [uploaded_file.name for uploaded_file in uploaded_files]

        # Save the uploaded files to the new directory
        for uploaded_file, file_name in zip(uploaded_files, file_names):
            with open(os.path.join(folder_path, file_name), "wb") as f:
                f.write(uploaded_file.getbuffer())

        # Read each file from the new directory, add 'Tag' column with file name, and concatenate all files
        all_data = pd.concat(
            [
                pd.read_csv(os.path.join(folder_path, name)).assign(Tag=name)
                for name in file_names
            ]
        )

        # Perform data cleaning
        all_data["Found SERP"] = all_data["Found SERP"].str.replace(
            "https://", ""
        )  # Cleaning 1
        all_data["Found SERP"] = (
            all_data["Found SERP"].str.split("#").str[0]
        )  # Cleaning 2

        # Create new column
        all_data["search_key"] = (
            all_data["Found SERP"]
            + " | "
            + all_data["Keyword for: (lifepal.co.id/media)"]
        )

        # Save to a new CSV file in the new directory
        new_file_path = os.path.join(folder_path, "SERP All Data.csv")
        all_data.to_csv(new_file_path, index=False)

        # Display the dataframe as a table in the Streamlit app
        st.title("SEO Dashboard")
        st.dataframe(all_data)

        # Create a download button for the new file
        with open(new_file_path, "rb") as f:
            bytes_data = f.read()
        st.download_button(
            label="Download SERP All Data.csv",
            data=bytes_data,
            file_name="SERP All Data.csv",
            mime="text/csv",
        )
        st.write(
            "All files successfully combined, cleaned, and new column 'search_key' added. The updated data is saved to the 'new report' directory as 'SERP All Data.csv'"
        )

        if st.button("Update to Media O", key="update_media_o"):
            media_o = pd.read_csv(os.path.join(folder_path, "Media O.csv"))
            serp_data = pd.read_csv(os.path.join(folder_path, "SERP All Data.csv"))

            merged_data = media_o.merge(
                serp_data[["search_key", "www.google.co.id current position"]],
                on="search_key",
                how="left",
            )

            merged_data["Current Position"] = merged_data[
                "www.google.co.id current position"
            ].fillna(100)

            media_o["Current Position"] = merged_data["Current Position"]

            media_o.to_csv(os.path.join(folder_path, "Media O.csv"), index=False)
            st.write("Data updated successfully.")
