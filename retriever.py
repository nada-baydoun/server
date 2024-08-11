import chromadb

# Initialize Chroma client and collection
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection1")

def build_and_clean_arrays_from_rawdata(file_path):
    ids = []
    documents = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_id = None
    current_document = []

    for line in lines:
        line = line.strip()
        if line.startswith("ID: "):
            # Save the previous ID and document if they exist
            if current_id is not None:
                if not current_id.lower().startswith('id:'):
                    documents.append(' '.join(current_document).strip())
                    ids.append(current_id)

            # Start a new ID
            current_id = line[4:].strip()
            current_document = []
        elif line.startswith("Document: "):
            current_document.append(line[10:].strip())
        elif current_id is not None:
            # Continue adding lines to the current document if they are part of the document
            current_document.append(line.strip())

    # Append the last ID and document
    if current_id is not None and not current_id.lower().startswith('id:'):
        documents.append(' '.join(current_document).strip())
        ids.append(current_id)

    # Combine documents with duplicate IDs
    id_to_document = {}
    for id_, doc in zip(ids, documents):
        if id_ in id_to_document:
            id_to_document[id_].append(doc)
        else:
            id_to_document[id_] = [doc]

    # Clean up duplicates
    final_ids = []
    final_documents = []

    for id_, docs in id_to_document.items():
        combined_document = ' '.join(docs).strip()  # Combine documents with the same ID
        final_ids.append(id_)
        final_documents.append(combined_document)

    return final_ids, final_documents

# File path
rawdata_file = r"C:\Users\nada\Desktop\Headstarter\Project 3\chatbot\app\RAG\rawdata.txt"

# Build and clean the arrays
ids, documents = build_and_clean_arrays_from_rawdata(rawdata_file)

# Add documents and IDs to the collection
#collection.delete()  # Ensure the collection is empty before adding new data
collection.add(
    documents=documents,
    ids=ids
)

def retrieve_information(query_text):
    results = collection.query(
        query_texts=[query_text],
        n_results=1
    )
    return results['documents'][0][0] if results['documents'] else "No results found."

# Example usage
if __name__ == "__main__":
    query = "What is DSA?"
    results = retrieve_information(query)
    print("Results:", results)
