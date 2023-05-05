# import os
# import streamlit as st
# from llama_index import download_loader
# from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
# from llama_index import StorageContext, load_index_from_storage

# NotionPageReader = download_loader('NotionPageReader')

# integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")

# st.title("Henry proof of concept - Simple Query")

# def extract_page_id_from_link(link: str) -> str:
#     parts = link.split("/")
#     last_part = parts[-1]
#     reversed_last_part = last_part[::-1]
#     reversed_page_id = ""

#     for char in reversed_last_part:
#         if char == "-":
#             break
#         reversed_page_id += char

#     page_id = reversed_page_id[::-1]
#     return page_id

# # The provided URL
# url = "https://www.notion.so/Artificial-Intelligence-The-Future-is-Now-a7a0175b397a421abedd7a5a7a036d33"

# # Extract the page ID from the URL
# page_id = extract_page_id_from_link(url)
# page_ids = [page_id]

# # Create the index using the extracted page ID
# reader = NotionPageReader(integration_token=integration_token)
# documents = reader.load_data(page_ids=page_ids)
# index = GPTVectorStoreIndex.from_documents(documents)
# index.storage_context.persist()

# # Load the index
# storage_context = StorageContext.from_defaults(persist_dir="./storage")
# loaded_index = load_index_from_storage(storage_context)
# query_engine = loaded_index.as_query_engine()

# # Add the query_engine to the session state
# if "query_engine" not in st.session_state:
#     st.session_state.index = query_engine

# # Text input field for the query
# query_text = st.text_input("Enter your query:", "")

# # Button to perform the query
# ask_button = st.button("Ask")

# if ask_button:
#     if not query_text:
#         st.error("Please enter a valid query.")
#     else:
#         # Perform the query and display the results
#         query_results = st.session_state.index.query(query_text)
#         st.write(query_results.response)
