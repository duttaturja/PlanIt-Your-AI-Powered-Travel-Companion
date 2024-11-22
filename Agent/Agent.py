"""
LLM interface functionality for DocuBuddy.
Handles language model operations and conversation management.
"""

import logging
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TravelAgent:

    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2:1b")
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are PlanIT, an expert AI travel companion. "
                "Help users plan their trips by providing detailed, "
                "personalized travel recommendations and itineraries. "
                "Focus on understanding the user's travel preferences, "
                "budget constraints, and specific interests."
            )),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()

    def chat(self, user_input: str) -> str:
        logger.info(f"User: {user_input}")
        chat_history = self.memory.load_memory_variables({})["chat_history"]
        response = self.chain.invoke({
            "input": user_input,
            "chat_history": chat_history
        })
        self.memory.save_context(
            {"input": user_input},
            {"output": response}
        )
        logger.info(f"Agent: {response}")
        return response

    def clear_history(self):
        self.memory.clear()
        logger.info("Chat history cleared")

if __name__ == "__main__":
    agent = TravelAgent()
    print("\nWelcome to PlanIT - Your AI Travel Companion!")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.\n")
    print("Agent: Hello! I'm here to help plan your next adventure. What kind of trip are you thinking about?")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nAgent: Goodbye! Have a great trip!")
                break
            
            if user_input:
                response = agent.chat(user_input)
                print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nAgent: Goodbye! Have a great trip!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Agent: I apologize, but I encountered an error. Please try again.")
