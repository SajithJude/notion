import os
import streamlit as st
from llama_index import download_loader
# from streamlit.script_runner import RerunException
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
import openai 

import re
def extract_page_id_from_link(link: str) -> str:
    # Split the link into parts by '/'
    parts = link.split("/")
    # Take the last part which should contain the page ID
    last_part = parts[-1]

    # Reverse the last part
    reversed_last_part = last_part[::-1]

    # Initialize the reversed_page_id
    reversed_page_id = ""

    # Iterate through the reversed_last_part, and append characters until a hyphen is encountered
    for char in reversed_last_part:
        if char == "-":
            break
        reversed_page_id += char

    # Reverse the reversed_page_id to get the actual page_id
    page_id = reversed_page_id[::-1]

    # Format the page ID by inserting hyphens in the correct pattern: 8-4-4-4-12
    # formatted_page_id = f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"

    return page_id


# documents = SimpleDirectoryReader('data').load_data()

NotionPageReader = download_loader('NotionPageReader')

integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Henry")

# Selection of Notion type
option = st.selectbox(
    "Select the Notion element type",
    ("Database", "Page")
)

# Input field for ID
# Input field for the link
# Input field for the links
page_links = st.text_area("Enter the Notion {} links (separate by comma or newline):".format(option), "")

# Button to load data
load_data_button = st.button("create index")

if load_data_button:
    if not page_links:
        st.error("Please enter valid Notion {} links.".format(option))
    else:
        # Extract the page IDs from the links
        links = [link.strip() for link in page_links.replace(',', '\n').split('\n') if link.strip()]
        pageids = [extract_page_id_from_link(link) for link in links]
        st.write(pageids)
        reader = NotionPageReader(integration_token=integration_token)

        if option == "Database":
            documents = []
            for page_id in pageids:
                documents.extend(reader.load_data(database_id=page_id))
                databaseindex = GPTVectorStoreIndex.from_documents(documents)
                databaseindex.storage_context.persist()
        else:
            documents = reader.load_data(page_ids=pageids)
            pageindex = GPTVectorStoreIndex.from_documents(documents)
            pageindex.storage_context.persist()

# # Button to load index
# load_index_button = st.button("Load Saved Index")

# if load_index_button:
    # Rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        # Load index
        loaded_index = load_index_from_storage(storage_context)
        query_engine = loaded_index.as_query_engine()
        if "query_engine" not in st.session_state:
            st.session_state.index= query_engine
        st.success("Index loaded successfully!")
        # st.info("Index information:", query_engine)


if "query_engine" not in st.session_state:
    query_text = st.text_input("Enter your query:", "")
    # Button to perform the query
    ask_button = st.button("Ask")


if ask_button:
    query_results = st.session_state.index.query(query_text)
    st.write(query_results.response)

    # if not query_text:
    #     st.error("Please enter a valid query.")
    # else:
    #     # Make sure the index is loaded before performing the query
    #     if not query_engine:
    #         st.error("Please load the index before querying.")
    #     else:
    #         # Perform the query and display the results
            