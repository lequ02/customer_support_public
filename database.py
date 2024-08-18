import json
import faiss
import tensorflow as tf
from sentence_transformers import SentenceTransformer # cant import globally due to tensorflow conflict with sentence_transformers


# Function to extract relevant text and metadata from a complaint
def extract_text_and_metadata(complaint):
    metadata = {
        'product': complaint['_source']['product'],
        'sub_product': complaint['_source']['sub_product'],
        'issue': complaint['_source']['issue'],
        'sub_issue': complaint['_source']['sub_issue']
    }
    # text = f"{metadata['product']} {metadata['sub_product']} {metadata['issue']} {metadata['sub_issue']} {complaint['_source']['complaint_what_happened']}"
    text = f"{complaint['_source']['complaint_what_happened']}"

    return text, metadata

# Function to initialize the vector database with the given complaints
def initialize_db(complaints):
    # from sentence_transformers import SentenceTransformer
    # Extract text and metadata from each complaint
    texts = []
    metadata_list = []
    for complaint in complaints:
        text, metadata = extract_text_and_metadata(complaint)
        if text and metadata:  # Ensure both text and metadata are present
            texts.append(text)
            metadata_list.append({'metadata': metadata, 'text': text})

    # Generate embeddings using a pre-trained SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)

    # Initialize FAISS index with the appropriate dimension
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save the index and metadata
    faiss.write_index(index, "complaint_embeddings.index")
    with open("metadata_list.json", "w") as meta_file:
        json.dump(metadata_list, meta_file)

# Function to add new complaints to the existing vector database
def save_complaint_to_db(text, metadata, model=None):
    # from sentence_transformers import SentenceTransformer
    # Load the existing index and metadata
    index = faiss.read_index("complaint_embeddings.index")
    with open("metadata_list.json", "r") as meta_file:
        metadata_list = json.load(meta_file)
    
    # Use the provided model or initialize a new one
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')

    # Extract text and generate the embedding for the new complaint
    new_text, new_metadata = text, metadata
    if new_text and new_metadata:  # Ensure both text and metadata are present
        new_embedding = model.encode([new_text])

        # Add the new embedding and metadata to the index
        index.add(new_embedding)
        metadata_list.append({'metadata': new_metadata, 'text': new_text})

        # Save the updated index and metadata
        faiss.write_index(index, "new_complaint_embeddings.index")
        with open("metadata_list.json", "w") as meta_file:
            json.dump(metadata_list, meta_file)
    else:
        print("Error: Missing text or metadata for the new complaint.")

# Function to search the vector database for similar complaints
def search_similar_complaints(query, k=5):
    # from sentence_transformers import SentenceTransformer
    # Load the existing index and metadata
    index = faiss.read_index("complaint_embeddings.index")
    with open("metadata_list.json", "r") as meta_file:
        metadata_list = json.load(meta_file)
    
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Generate the embedding for the query
    query_vector = model.encode([query])

    # Search for the top k similar complaints
    distances, indices = index.search(query_vector, k)

    # Return the metadata, text, and distances of the similar complaints
    similar_complaints = []
    for idx, dist in zip(indices[0], distances[0]):
        complaint_info = metadata_list[idx]
        # Ensure the dictionary has both 'metadata' and 'text' keys
        if 'metadata' in complaint_info and 'text' in complaint_info:
            similar_complaints.append({
                'metadata': complaint_info['metadata'],
                'text': complaint_info['text'],
                'distance': dist
            })
        else:
            print(f"Error: Missing 'metadata' or 'text' in entry at index {idx}")
            print(f"info {complaint_info}")  # Print out the problematic entry

    return similar_complaints

def main():
    # Load the complaints data from JSON
    with open('ruby_hackathon_data.json', 'r') as f:
        complaints = json.load(f)
    
    ## Initialize the vector database with the loaded complaints
    initialize_db(complaints)
    
    # Example query to search the database
    query = "Credit card dispute"
    results = search_similar_complaints(query)
    
    # Print out the results
    for result in results:
        metadata = result['metadata']
        text = result['text']
        distance = result['distance']
        print(f"Distance: {distance}")
        print(f"Product: {metadata['product']}")
        print(f"Sub-product: {metadata['sub_product']}")
        print(f"Issue: {metadata['issue']}")
        print(f"Sub-issue: {metadata['sub_issue']}")
        print(f"Complaint Text: {text}")
        print()

    # save_complaint_to_db(query)  # Add the query as a new complaint to the database

if __name__ == '__main__':
    main()
