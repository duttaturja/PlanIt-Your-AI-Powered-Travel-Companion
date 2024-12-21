import os
import logging
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TravelAgent:
    def __init__(self):
        self.api = OpenAI(api_key="", base_url="https://api.aimlapi.com/v1")
        self.system_prompt ="You are a travel agent. Provide descriptive, personalized travel advice based on the user's preferences and questions."
        self.chat_history = []
        self.entities = {}

    def chat(self, user_input):
        """Generate AI response with chat history and entity context."""
        messages = ([{"role": "system", "content": self.system_prompt}] +
                    self.chat_history +
                    [{"role": "user", "content": user_input}])

        try:
            completion = self.api.chat.completions.create(
                model="GPT-4",
                messages=messages,
                temperature=0.7,
                max_tokens=256,
            )
            response = completion.choices[0].message.content
            self._update_context(user_input, response)
            self._extract_entities(user_input)
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm sorry, I couldn't process your request. Please try again."

    def _update_context(self, user_input, response):
        """Update chat history with the latest interaction."""
        self.chat_history.extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response}
        ])

    def _extract_entities(self, user_input):
        """Extract simple entities based on predefined keywords."""
        entity_keywords = {
            "destinations": ["travel to", "visit", "destination", "go to"],
            "budget": ["budget", "cost", "spend", "price"],
            "dates": ["date", "when", "schedule", "duration"],
        }
        for entity, keywords in entity_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                self.entities[entity] = user_input

    def clear_history(self):
        """Clear chat history and entities."""
        self.chat_history.clear()
        self.entities.clear()
        logger.info("Chat history and entities cleared.")

if __name__ == "__main__":
    API_KEY = "6defa90e7edf4d5ba0794a2a49a7091c"
    BASE_URL = "https://api.aimlapi.com/v1"
    SYSTEM_PROMPT = (
        "You are a travel agent. Provide descriptive, personalized travel advice "
        "based on the user's preferences and questions."
    )

    agent = TravelAgentOpenAI(api_key=API_KEY, base_url=BASE_URL, system_prompt=SYSTEM_PROMPT)

    print("\nWelcome to TravelBot! Type 'exit' to end the conversation.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("Agent: Goodbye! Safe travels!")
            break
        print(f"Agent: {agent.chat(user_input)}")
