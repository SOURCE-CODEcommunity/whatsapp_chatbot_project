import requests

def chat_with_huggingface(user_input):
    try:
        url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
        headers = {"Authorization": f"Bearer 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"}
        data = {"inputs": user_input}
        
        response = requests.post(url, headers=headers, json=data)
        # print(response.json())
        return response.json()[0]['generated_text']
    except Exception as e:
        return "*There was an error please Try again!, Thank you*"
