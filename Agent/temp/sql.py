import os
import logging
from typing import Dict, Any
from langchain.memory.entity import SQLiteEntityStore
from langchain.memory import ConversationEntityMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TravelAgentEntityMemory:

    def __init__(self):
        # Initialize LLM with llama model
        self.llm = OllamaLLM(model="llama3.2")
        
        # Set up database path in the temp directory
        db_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Initialize entity memory with configuration
        self.memory = ConversationEntityMemory(
            llm=self.llm,
            entity_store=SQLiteEntityStore(
                database_path=os.path.join(db_dir, "entities.db")
            ),
            input_key="input",
            output_key="output",
            return_messages=True,
            k=10  # Remember last 10 entity mentions
        )

        # Define the prompt with better context handling
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You are PlanIT, an expert AI travel companion. "
                "Help users plan their trips by providing detailed, "
                "personalized travel recommendations and itineraries. "
                "Focus on understanding the user's travel preferences, "
                "budget constraints, and specific interests. "
                "Use the provided entity information to maintain context."
            )),
            MessagesPlaceholder(variable_name="history"),
            MessagesPlaceholder(variable_name="entities"),
            ("human", "{input}")
        ])

        # Create a processing chain
        self.chain = self.prompt | self.llm | StrOutputParser()

    def chat(self, user_input: str) -> str:
        try:
            # Load memory variables
            memory_vars = self.memory.load_memory_variables({"input": user_input})
            print("Memory Variables:", memory_vars)
            chat_history = memory_vars.get("history", [])
            print("Chat History:", chat_history)
            entities = memory_vars.get("entities", {})
            print("Entities:", entities)
            
            # Format entity context as messages
            entity_messages = []
            if entities:
                entity_lines = []
                for category, info in entities.items():
                    if info:
                        entity_lines.append(f"{category.title()}: {info}")
                if entity_lines:
                    entity_content = "\n".join(entity_lines)
                    entity_messages = [SystemMessage(content=f"Known entities:\n{entity_content}")]
            
            # Generate response with context
            response = self.chain.invoke({
                "input": user_input,
                "history": chat_history,
                "entities": entity_messages
            })
            
            # Save context
            self.memory.save_context(
                {"input": user_input},
                {"output": response}
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            return "I apologize, but I encountered an error. Please try again."

    def clear_history(self):
        try:
            self.memory.clear()
            logger.info("Memory cleared")
        except Exception as e:
            logger.error(f"Error clearing history: {str(e)}")

if __name__ == "__main__":
    agent = TravelAgentEntityMemory()
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
