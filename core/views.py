from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Agent.Agent import TravelAgent
from django.views.decorators.csrf import csrf_exempt
import json

# Initialize the TravelAgent as a global instance
travel_agent = TravelAgent()

def index(request):
    return render(request, "index.html")

@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Get response from travel agent
            response = travel_agent.chat(user_message)
            
            return JsonResponse({
                'response': response,
                'status': 'success'
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def profile(request):
    return render(request, "account/profile.html")

@csrf_exempt
def clear_chat(request):
    if request.method == "POST":
        try:
            travel_agent.clear_history()
            return JsonResponse({
                'status': 'success',
                'message': 'Chat history cleared'
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)