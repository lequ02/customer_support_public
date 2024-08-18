# def main(product_name, complaint_text, file_paths, audio_path):
#     # Placeholder for your main processing function
#     # Replace this with your actual implementation
#     response_json = {"status": "processed"}
    
#     components = []
#     if product_name:
#         components.append(f"product '{product_name}'")
#     if complaint_text:
#         components.append(f"a text complaint of {len(complaint_text)} characters")
#     if file_paths:
#         components.append(f"{len(file_paths)} file(s)")
#     if audio_path:
#         components.append("an audio recording")
    
#     complaint_description = " and ".join(components)
#     response_content = f"Your complaint has been processed. We received {complaint_description}."
    
#     return response_json, response_content

import faiss
import json

# Load the index
index = faiss.read_index("complaint_embeddings.index")

# Get the number of items in the index
num_items = index.ntotal

print(f"Number of items in the index: {num_items}")


# Read metadata_list.json
with open("metadata_list.json", "r") as f:
    metadata_list = json.load(f)

# Process the metadata_list
# Replace this with your actual implementation
processed_metadata = metadata_list[:10]

# Print the processed metadata
print(processed_metadata)
