import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import pandas as pd

# Initialize connection to Elasticsearch
es = Elasticsearch(
    'https://localhost:9200',
    basic_auth=('elastic', 'epd1di6ZdaxYfLp0qmep'),
    ca_certs='C:/elasticsearch/elasticsearch-8.13.4/config/certs/http_ca.crt'
)

# Load the pre-trained Sentence Transformer model
model = SentenceTransformer("all-mpnet-base-v2")

# Dummy brand options


# Streamlit application starts here
st.title('AI Style Assistant: Discover Your Perfect Look (Semantic Search Engine)')

# Search bar
user_query = st.text_input("Enter a keyword to search for products:", "")

# Dummy brand selection drop-down


if user_query:
    # Encode the user's query using the same model used for indexing
    query_vector = model.encode(user_query).tolist()  # Convert to list for JSON serialization

    # Elasticsearch query
    query = {
        "size": 10,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'description_vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }

    # Fetch results from Elasticsearch
    results = es.search(index='all_product', body=query)

    # Check if there are results
    if results['hits']['hits']:
        st.subheader('Search Results:')
        for hit in results['hits']['hits']:
            st.write(f"**Product Name:** {hit['_source']['ProductName']}")
            st.write(f"**Description:** {hit['_source']['Description']}")
            st.write("-----")
    else:
        st.subheader('No results found.')
