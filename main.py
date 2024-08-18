from text_processing import summarize
from speech2text import transcribe_audio
from rag import get_similar_complaints, generate_response_openrouter, positive_generate_response_openrouter
from ocr import ocr_space_file
import json
from concurrent.futures import ThreadPoolExecutor
from classifier import sub_product_classifier, product_classifier
# import tensorflow as tf
# import keras
from database import save_complaint_to_db

def main(product_name, complaint_text, file_paths, audio_path):
    executor = ThreadPoolExecutor(max_workers=2)
    text = ""
    if audio_path:
        text += "Audio complaint: " + transcribe_audio(audio_path) + "\n\n"

    if complaint_text:
        text += "Text complaint: " + complaint_text + "\n\n"
    if file_paths:
        for path in file_paths:
            string = ocr_space_file(filename=path, language='eng', overlay=False)
            result_dict = json.loads(string)
            img_content = result_dict['ParsedResults'][0]['ParsedText'].replace('\r', ' ').replace('\n', ' ')

            text += "Image complaint: " + img_content

    json_file, summary_complaint = summarize(text)

    if summary_complaint == 'Not a complaint':
        print('Not a complaint')
        response_json, response_content = positive_generate_response_openrouter(text)
        return response_json, response_content, None
    else:
        print('Complaint Summary:', summary_complaint)

        # Run rag_response and save_to_db concurrently
        future_rag = executor.submit(rag_response, text)
        future_save = executor.submit(save_to_db, product_name, text)

        # Wait for rag_response to complete and get the result
        response_json, response_content = future_rag.result()

        # We don't wait for save_to_db to complete here, but we return the future
        return response_json, response_content, future_save


def rag_response(text):
    similar_complaints = get_similar_complaints(text)
    response_json, response_content = generate_response_openrouter(text, similar_complaints)
    # print("\nGenerated Response:")
    # print(response_content)


    # response_json, response_content = "dummy1", "dummy2"
    return response_json, response_content

def save_to_db(product_name, complaint_text):
    print("\n\n\nComplaint Text:", complaint_text)
    sub_product = sub_product_classifier(complaint_text)
    # print("Sub Product:", sub_product)
    if not product_name:
        product_name = product_classifier(complaint_text)
    # print("Product:", product_name)
    metadata = {
        'product': product_name,
        'sub_product': sub_product,
        'issue': None,
        'sub_issue': None
    }
    save_complaint_to_db(text = complaint_text, metadata = metadata)

    # pass

    # print("\n\n\nComplaint saved to database.\n\n\n")
    return "save_to_db completed"  # Add this line to return a completion signal

if __name__ == '__main__':
    import time

    start_time = time.time()
    product_name = ""
    complaint_text = "I have a problem with my credit card charges. There are several transactions I don't recognize, and I'm worried my card has been compromised."
    file_paths = []
    audio_path = None

    main(product_name = product_name, 
        complaint_text = complaint_text, 
        file_paths = file_paths, 
        audio_path = audio_path)

    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution Time:", execution_time, "seconds")


    # save_to_db("Credit card", "I have a problem with my credit card charges. There are several transactions I don't recognize, and I'm worried my card has been compromised.", [], None)

    # import classifier
    # classifier.main()