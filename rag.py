import json
import faiss
import numpy as np
import openai
import os
import requests
from sentence_transformers import SentenceTransformer


# Set up OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_key = "*************************"


def extract_text(complaint):
    source = complaint['_source']
    return f"{source['product']} {source['sub_product']} {source['issue']} {source['sub_issue']} {source['complaint_what_happened']}"

# texts = [extract_text(complaint) for complaint in complaints]

# # Create embeddings
# model = SentenceTransformer('all-MiniLM-L6-v2')
# embeddings = model.encode(texts)

# # Create and save the FAISS index
# dimension = embeddings.shape[1]
# index = faiss.IndexFlatL2(dimension)
# index.add(embeddings)
# faiss.write_index(index, "complaint_embeddings.index")


# Function to retrieve similar complaints
def get_similar_complaints(query, model=None, k=5):
    # from sentence_transformers import SentenceTransformer

    # Load and prepare data
    with open('ruby_hackathon_data.json', 'r') as f:
        complaints = json.load(f)
    # with open('metadata_list.json', 'r') as f:
    #     complaints = json.load(f)
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("complaint_embeddings.index")
    query_vector = model.encode([query])

    # print("query_vector", query_vector)
    

    distances, indices = index.search(query_vector, k)

    # print("indices", indices)
    # print("distances", distances)

    return [complaints[i] for i in indices[0]]

# Function to format complaints for GPT-3 context
def format_complaints_for_context(similar_complaints):
    context = "Here are some similar complaints for reference:\n\n"
    for i, complaint in enumerate(similar_complaints, 1):
        source = complaint['_source']
        context += f"{i}. Product: {source['product']}\n"
        context += f"   Issue: {source['issue']}\n"
        context += f"   Complaint: {source['complaint_what_happened'][:200]}...\n\n"
        context += f"   Company response: {source['company_response']}\n"
        context += f"   Company public response: {source['company_public_response']}\n\n"
    return context

# Function to generate response using GPT-3
def generate_response_gpt(query, similar_complaints):
    context = format_complaints_for_context(similar_complaints)
    prompt = f"""Given the following complaint and context of similar complaints, provide a helpful response addressing the issue and suggesting potential solutions. Be empathetic and professional.

New complaint: {query}

{context}

Response:"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI customer service assistant for a financial institution."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].message['content'].strip()


OPENROUTER_API_KEY = "********************"

# Function to generate response using openrouter.ai
def generate_response_openrouter(query, similar_complaints):
    context = format_complaints_for_context(similar_complaints)
    prompt = f"""Given the following complaint and context of similar complaints, provide a helpful response addressing the issue and suggesting potential solutions. Be empathetic and professional.

New complaint: {query}

{context}

Response:"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            # "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
            # "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
        },
        data=json.dumps({
            "model": "openai/gpt-3.5-turbo", # Optional
           "messages": [
            {"role": "system", "content": "You are a helpful AI customer service assistant for a financial institution. Sign the response as 'Smart Support'."},
            {"role": "user", "content": prompt}
        ],
        # "max_tokens": 300,
        # "n": 1,
        # "stop": None,
        # "temperature": 0.7
        })
        )

    summary_content = response.json()["choices"][0]["message"]["content"]

    return response.json(), summary_content


def positive_generate_response_openrouter(query, similar_feedbacks=None):

    # this can be used to suggest customer to different products or services


    # context = format_complaints_for_context(similar_feedbacks)
    prompt = f"""Given the following positive feedback from a customer, provide a helpful response. Be grateful and professional.

Feedback: {query}

Response:"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            # "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
            # "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
        },
        data=json.dumps({
            "model": "openai/gpt-3.5-turbo", # Optional
           "messages": [
            {"role": "system", "content": "You are a helpful AI customer service assistant for a financial institution. Sign the response as 'Smart Support'."},
            {"role": "user", "content": prompt}
        ],
        # "max_tokens": 300,
        # "n": 1,
        # "stop": None,
        # "temperature": 0.7
        })
        )

    summary_content = response.json()["choices"][0]["message"]["content"]

    return response.json(), summary_content

def main():
    # Example usage
    new_complaint = "I have a problem with my credit card charges. There are several transactions I don't recognize, and I'm worried my card has been compromised."
    similar_complaints = get_similar_complaints(new_complaint)

    print("Most similar complaints:")
    for complaint in similar_complaints:
        print(f"Product: {complaint['_source']['product']}")
        print(f"Issue: {complaint['_source']['issue']}")
        print(f"Complaint: {complaint['_source']['complaint_what_happened'][:100]}...")
        print(f"   Company response: {complaint['_source']['company_response']}")
        print(f"   Company public response: {complaint['_source']['company_public_response']}")
        print("---")

    response_json, response_content = generate_response_openrouter(new_complaint, similar_complaints)
    print("\nGenerated Response:")
    print(response_content)

if __name__ == '__main__':
    main()