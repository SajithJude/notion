import os
import streamlit as st
from llama_index import download_loader
# from streamlit.script_runner import RerunException
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
import openai 


# documents = SimpleDirectoryReader('data').load_data()

NotionPageReader = download_loader('NotionPageReader')

integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Notion Page Reader")

# Selection of Notion type
option = st.selectbox(
    "Select the Notion element type",
    ("Database", "Page")
)

# Input field for ID
page_id = st.text_input("Enter the Notion {} ID:".format(option), "")

# Button to load data
load_data_button = st.button("create index")

if load_data_button:
    if not page_id:
        st.error("Please enter a valid Notion {} ID.".format(option))
        # raise RerunException(st.script_request_queue.RerunData(None))

    reader = NotionPageReader(integration_token=integration_token)

    if option == "Database":
        documents = reader.load_data_from_database(database_id=page_id)
        databseindex  = GPTVectorStoreIndex.from_documents(documents)
        databseindex.storage_context.persist()
    else:
        documents = reader.load_data_from_page(page_id=page_id)
        pageindex  = GPTVectorStoreIndex.from_documents(documents)
        databseindex.storage_context.persist()


# Button to load index
load_index_button = st.button("Load Saved Index")

if load_index_button:
    # Rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    # Load index
    loaded_index = load_index_from_storage(storage_context)
    query_engine = loaded_index.as_query_engine()
    if "query_engine" not in st.session_state:
        st.session_state.index= query_engine
    st.success("Index loaded successfully!")
    st.info("Index information:", query_engine)


if "query_engine" not in st.session_state:
    query_text = st.text_input("Enter your query:", "")
    # Button to perform the query
    ask_button = st.button("Ask")


if ask_button:
    if not query_text:
        st.error("Please enter a valid query.")
    else:
        # Make sure the index is loaded before performing the query
        if not query_engine:
            st.error("Please load the index before querying.")
        else:
            # Perform the query and display the results
            query_results = query_engine.query(query_text)
            st.write("Query results:", query_results)
