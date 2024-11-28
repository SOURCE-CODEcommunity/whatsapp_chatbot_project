# from django.shortcuts import render
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .huggingface_helper import chat_with_huggingface

#Whatsapp Business API access token
WHATSAPP_API_TOKEN = "EAARMPZAdjRHEBO5RKo5zVYefztX43AFA002yUNjmx2bBx4mtpvKfwbBZCYM5i58rhP4RtzF4T4PZBvtTUhD8jLL9fIQRiZCZBAokIewC30e7h8Ym70qXccegMjfzqXi33mD93LzbLoNxZAwXGo6X0YZCXtwBXArW6Cha4HNUIr6et4hrzTbpcFfZC0EzKZCmDsUFQM4fFbLrCCquzp37gx6t4KYnqEZBEZD"
#Whatsapp Business API endpoint
WHATSAPP_API_URL = "https://graph.facebook.com/v21.0/524548570731447/messages"

# Create your views here.

@csrf_exempt
def whatsapp_webhook(request):
    #Handle Post request for message processing
    if request.method == "POST":
        data = json.loads(request.body)
        print(json.dumps(data, indent=4)) 

        # Process the incoming message
        # Check if this is a message from the user
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                if "messages" in change.get("value", {}):  # Correct key: 'value'
                    for message in change["value"]["messages"]:
                        sender_id = message["from"]  # The user's phone number
                        message_type = message["type"]

                        if message_type == "text":
                            text = message["text"]["body"]
                            response_text = chat_with_huggingface(text)
                        elif message_type == "image":
                            response_text = "I received an image, but i can only respond to text at the moment"
                        else:
                            response_text = "Unsupported message type"

                        #Send the response back to the user
                        send_whatsapp_message(sender_id, response_text)
    
        return JsonResponse({'status': "received"}, status=200)
    else:
        #Handle Get request for webhook verification
        verify_token = "chatbot_secure_8_2024"
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        #Check if mode and token are correct
        if mode == "subscribe" and token == verify_token:
            return HttpResponse(challenge)
        else:
            return JsonResponse({"error": "invalid token"}, status=403)

def send_whatsapp_message(sender_id, response):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": f"{sender_id}",
        "text": {"body": response}
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)

    #Log the response status and content for debugging
    print(f"Response Status: {response.status_code}")
    print(f"Response Content: {response.content}")

    return response
