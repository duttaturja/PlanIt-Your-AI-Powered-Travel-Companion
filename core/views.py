from django.shortcuts import render
from Agent.Agent import TravelAgent
import logging

logger = logging.getLogger(__name__)

# Initialize the TravelAgent as a global instance
travel_agent = TravelAgent()

def index(request):
    context = {
        'messages': request.session.get('chat_history', []),
        'error': None
    }
    
    if request.method == "POST":
        try:
            user_message = request.POST.get('message', '').strip()
            if user_message:
                # Add user message to history
                chat_history = request.session.get('chat_history', [])
                chat_history.append({
                    'role': 'user',
                    'content': user_message
                })
                
                # Get AI response
                response = travel_agent.chat(user_message)
                
                if response:
                    chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
                    request.session['chat_history'] = chat_history
                    context['messages'] = chat_history
                else:
                    context['error'] = "Sorry, I couldn't generate a response. Please try again."
            else:
                context['error'] = "Please enter a message."
                
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            context['error'] = "An error occurred. Please try again."
    
    return render(request, "index.html", context)