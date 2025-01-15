from django.shortcuts import render
import finnhub
from django.http import JsonResponse
import requests
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from bs4 import BeautifulSoup


def post_list(request):
        finnhub_client = finnhub.Client(api_key="cmnqpqhr01qs0nh7qfa0cmnqpqhr01qs0nh7qfag")
        investment_news = finnhub_client.general_news('general', min_id=0)

        # return render(request, 'portfolio/post_list.html', {})
        return render(request, 'portfolio/post_list.html', {'investment_news': investment_news})


def database(request):
        return render(request, 'portfolio/Database.html',{})


import requests

def get_gpt3_response(user_input, api_key):
    print("API Key:", api_key)
    endpoint = 'https://api.openai.com/v1/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    data = {
        'prompt': user_input,
        'max_tokens': 100,
    }
    try:
        response = requests.post(endpoint, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP errors
        text = response.json()['choices'][0]['text']
    except requests.exceptions.RequestException as e:
        text = f"Error: {e}"
    except (KeyError, IndexError):
        text = "Error: Unexpected response format from AI model"
    return text



def user_logout(request):
    logout(request)
    return redirect('post_list')  # Redirect to the desired page after logout

import spacy
from django.shortcuts import render
from django.http import JsonResponse

def chat(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        print("Received text:", text)  # Debugging print statement
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
        print("Identified entities:", entities)  # Debugging print statement
        return JsonResponse({'entities': entities})
    return render(request, 'portfolio/chat.html')

import spacy
from django.http import JsonResponse

def analyze_text(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
        return JsonResponse({'entities': entities})
    else:
        return JsonResponse({'error': 'Invalid request method'})
