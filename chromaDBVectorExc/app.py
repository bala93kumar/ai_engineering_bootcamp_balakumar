import chromadb

# Initialize the Chroma client
chroma_client = chromadb.Client()

# Create or get the collection
collection = chroma_client.get_or_create_collection(name="my_collection")

documents = [
    {"id": "doc1", "text": "HOW ARE YOU TODAY"},
    {"id": "doc2", "text": "goodBy see you later"}, 
    {"id": "doc3", "text": "Hello world"}
]

query = "hello world"

# Extract IDs and texts into lists for a single batch upsert
ids = [doc["id"] for doc in documents]
texts = [doc["text"] for doc in documents]

# Upsert the documents (use 'documents' instead of 'text', and pass them as lists)
collection.upsert(ids=ids, documents=texts)

query_text = "hello World"
# Query the collection
results = collection.query(query_texts=query_text, n_results=3)
print(results)
