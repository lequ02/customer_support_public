import numpy as np
import json
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import keras

def sub_product_classifier(new_complaint):
    # Load JSON data
    with open('ruby_hackathon_data.json', 'r') as file:
        complaints = json.load(file)

    # Convert JSON data to DataFrame
    df = pd.DataFrame([complaint['_source'] for complaint in complaints])

    # Preprocess the data
    X = df['complaint_what_happened'].values
    y = df['sub_product'].values
    # Encode the target variable
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Define the TextVectorization layer with padding
    vectorizer = keras.layers.TextVectorization(output_mode='int')
    vectorizer.adapt(X)


    model = keras.models.load_model('best_model (2).keras')
    
    # Preprocess the new complaint
    new_complaint_sequence = vectorizer([new_complaint])

    # Predict the sub-product for the new complaint
    prediction = model.predict(new_complaint_sequence)
    predicted_sub_product = label_encoder.inverse_transform([np.argmax(prediction)])

    print('Predicted sub_product:', predicted_sub_product[0])

    return predicted_sub_product[0]




def product_classifier(text):
    # there's only one product in the dataset
    print("Product: Credit card")
    return "Credit card"


def main():
    import time
    start_time = time.time()

    # new_complaint = "I purchased a XXXX XXXX XXXX XXXX on XX/XX/XXXX, using my TD BANK XXXX XXXX credit account. Phone was supposed to be delivered XX/XX/XXXX. Instead I get a delivery delayed notice. I contact XXXX and they tell me they will not ship the phone because XXXXXXXX XXXX was not authorizing the transaction. I reached out to XXXXXXXX XXXX and waited in cues a total of over 6 hours only to be hung up on 2 times. I also emailed their listed customer service department seeking help, because once I logged into my account not only did I find that they did authorize the transaction on XX/XX/XXXX, they authorized it again on XX/XX/XXXX. My current card balance is sitting at double, so {$2400.00}. But even with proof that the transaction is complete, XXXX is not releasing the product I was charged for twice."

    new_complaint = "I have a problem with my credit card charges. There are several transactions I don't recognize, and I'm worried my card has been compromised."
    product = product_classifier(new_complaint)
    sub_product = sub_product_classifier(new_complaint)
    print(f"Product: {product}, Sub-product: {sub_product}")


    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

if __name__ == '__main__':
    main()
