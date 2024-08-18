import faiss
from sentence_transformers import SentenceTransformer
import json


with open('ruby_hackathon_data.json', 'r') as f:
    complaints = json.load(f)


model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the index
index = faiss.read_index("complaint_embeddings.index")

# Search for similar complaints
query = "Credit card dispute"
query_vector = model.encode([query])
k = 5  # number of nearest neighbors to retrieve
distances, indices = index.search(query_vector, k)

# Retrieve the original complaints
similar_complaints = [complaints[i] for i in indices[0]]

print(similar_complaints)