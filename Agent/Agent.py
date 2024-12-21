"""
LLM interface functionality for PlanIT.
Handles language model operations and conversation management.
"""

import logging
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import SQLiteEntityStore, ConversationBufferMemory
from langchain.llms import OpenAI# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TravelAgent:

    def __init__(self):
        # self.llm = ChatGroq(model="llama-3.2-3b-preview")
        self.llm = OllamaLLM(model="llama3.2:1b")
        # self.llm = OpenAI(
        #     api_key="6defa90e7edf4d5ba0794a2a49a7091c",
        #     base_url="https://api.aimlapi.com",
        # )

        
        # Initialize both entity store and conversation memory
        db_path = "travel_entities.db"
        self.entity_store = SQLiteEntityStore(
            db_file=db_path,
            table_name="travel_entities"
        )
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
        
        # Initialize conversation counter
        self.conversation_counter = int(self.entity_store.get("conversation_counter", default=0))
        
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are PlanIt, an expert AI travel companion. "
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
        # Get stored entities and chat history for context
        try:
            # Retrieve all stored entities
            entities = {
                "preferences": self.entity_store.get("preferences", default={}),
                "destinations": self.entity_store.get("destinations", default={}),
                "budget": self.entity_store.get("budget", default={}),
                "dates": self.entity_store.get("dates", default={}),
                "activities": self.entity_store.get("activities", default={}),
                "accommodation": self.entity_store.get("accommodation", default={}),
                "transportation": self.entity_store.get("transportation", default={}),
                "special_requirements": self.entity_store.get("special_requirements", default={})
            }
            
            # Retrieve last 10 conversations
            conversations = []
            for i in range(max(0, self.conversation_counter - 10), self.conversation_counter):
                conv = self.entity_store.get(f"conversation_{i}", default=None)
                if conv:
                    conversations.append(conv)
            
            # Build context from entities and recent conversations
            context = []
            if conversations:
                context.append("Recent Conversations:")
                context.extend(conversations[-10:])  # Only last 10
                context.append("")  # Empty line separator
            
            for entity_type, value in entities.items():
                if value:
                    formatted_type = entity_type.replace("_", " ").title()
                    context.append(f"{formatted_type}: {value}")
            context_str = "\n".join(context) if context else ""
            
        except Exception as e:
            logger.warning(f"Error retrieving entities: {e}")
            context_str = ""
        
        # Get conversation history
        chat_history = self.memory.load_memory_variables({})["chat_history"]
        
        # Generate response with both entity context and chat history
        response = self.chain.invoke({
            "input": f"{context_str}\n{user_input}" if context_str else user_input,
            "chat_history": chat_history
        })
        
        # Store the interaction in both memory systems
        try:
            # Update conversation memory
            self.memory.save_context(
                {"input": user_input},
                {"output": response}
            )
            
            # Store conversation in entity store
            conversation = f"User: {user_input}\nAgent: {response}"
            self.entity_store.set(f"conversation_{self.conversation_counter}", conversation)
            self.conversation_counter += 1
            self.entity_store.set("conversation_counter", self.conversation_counter)
            
            # Update stored entities based on user input
            input_lower = user_input.lower()
            
            # Store last interaction
            self.entity_store.set("last_interaction", user_input)
            
            # Extract and store entities based on patterns
            entity_patterns = {
                "preferences": ["prefer", "like", "want", "looking for"],
                "destinations": ["visit", "go to", "travel to", "destination"],
                "budget": ["budget", "cost", "spend", "price", "expensive", "cheap"],
                "dates": ["date", "when", "duration", "days", "nights", "schedule"],
                "activities": ["activity", "do", "experience", "see", "explore", "adventure"],
                "accommodation": ["hotel", "stay", "hostel", "airbnb", "resort", "room"],
                "transportation": ["transport", "flight", "train", "bus", "car", "taxi"],
                "special_requirements": ["require", "need", "dietary", "vegetarian", "vegan", "accessibility", "wheelchair"]
            }
            
            # Check each pattern and update corresponding entity
            for entity_type, patterns in entity_patterns.items():
                if any(pattern in input_lower for pattern in patterns):
                    current_value = self.entity_store.get(entity_type, default={})
                    # If it's a new value, store it; if existing, append it
                    if isinstance(current_value, dict):
                        self.entity_store.set(entity_type, user_input)
                    else:
                        self.entity_store.set(entity_type, f"{current_value}; {user_input}")
            
        except Exception as e:
            logger.warning(f"Error storing conversation or entities: {e}")
        
        return response

    def clear_history(self):
        try:
            # Clear conversation memory
            self.memory.clear()
            
            # Clear entity store
            self.entity_store.delete("preferences")
            self.entity_store.delete("destinations")
            self.entity_store.delete("budget")
            self.entity_store.delete("dates")
            self.entity_store.delete("activities")
            self.entity_store.delete("accommodation")
            self.entity_store.delete("transportation")
            self.entity_store.delete("special_requirements")
            self.entity_store.delete("last_interaction")
            
            # Clear conversation history
            for i in range(max(0, self.conversation_counter - 10), self.conversation_counter):
                self.entity_store.delete(f"conversation_{i}")
            self.conversation_counter = 0
            self.entity_store.set("conversation_counter", 0)
            
            logger.info("Conversation history and entity store cleared")
        except Exception as e:
            logger.warning(f"Error clearing history: {e}")

if __name__ == "__main__":
    agent = TravelAgent()
    print("\nWelcome to PlanIt - Your AI Travel Companion!")
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
