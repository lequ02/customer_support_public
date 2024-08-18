import requests
import json
def summarize(text):
    OPENROUTER_API_KEY = "*************"
    


    prompt = f"""Given a text, decide whether the text is a complaint or not. If it is not a complaint, return 'Not a complaint'. If it is a complaint, summarize the complaint. Only return the summary, don't return the classification result.
Text: {text}

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
        { "role": "user", "content": prompt }
        ]
        
    })
    )

    summary_content = response.json()["choices"][0]["message"]["content"]

    return response.json(), summary_content



if __name__ == '__main__':
    # text = "XXXX XXXX XXXX XXXX, XXXX  XXXX XXXX, NY XXXX XXXX XXXX Date To : Macys XXXX Inc XXXX XXXX XXXX XXXXXXXX XXXX XXXX, NY XXXX Attn : XXXX XXXX Executive Office Dear XXXX XXXX, My name is XXXX XXXX, and I am writing to address the ongoing issues with my Macys credit account ( Account Number : XXXX ). Despite multiple attempts to resolve these matters over the phone, I have not received the necessary assistance to correct the inaccuracies on my account. \n\nXXXX. Disputed Charge and Lack of Support : I have called Macys customer service many times to dispute a charge of {$31.00} and address other concerns. Each time, the representatives were either unwilling or unable to assist me effectively. Macys should have records of these calls to verify my repeated efforts. \nXXXX. Late Fee : I acknowledge the late fee of {$31.00} charged on XX/XX/year>, and its subsequent credit on XX/XX/year>. However, this does not resolve the main issue of incorrect reporting. \nXXXX Credit Reporting Inaccuracy : My account was reported as 30 days delinquent in XX/XX/year>. I have consistently disputed this information, stating that payments for XXXX and XX/XX/year> were made but not properly applied to my account. \n\nAdditional Impact : Due to this delinquency on my credit report, my auto insurance increased to {$330.00} per month. This has been a significant financial burden. \n\nI request that Macys conduct a comprehensive review, including the phone call records, and correct the inaccuracies on my account. Additionally, I request the removal of the disputed by consumer note from my credit report once the issue is resolved. \n\nAdditionally, I do not want any Macys advertisements sent to my apartment. \n\nI hope to resolve this matter amicably and promptly. Thank you for your attention to this important issue. \n\nSincerely, XXXX XXXX"
    text = 'the product is very good. There isnt anything i dont like about it.'
    json, summary_content = summarize(text)

    print(json)
    print(summary_content)