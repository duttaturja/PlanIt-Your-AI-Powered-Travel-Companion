import logging
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global memory dictionary to handle multiple chat histories
chat_memory = {}

# Function to get or create memory for a specific chat
def get_memory_for_chat(chat_id):
    if chat_id not in chat_memory:
        chat_memory[chat_id] = ConversationBufferMemory(
            return_messages=True  # Enables returning messages as objects
        )
    return chat_memory[chat_id]

class TravelAgent:

    def __init__(self):
        self.llm = OllamaLLM(model="qw")

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

    def chat(self, user_input: str, session) -> str:
        try:
            # Retrieve chat history from the session
            chat_history = session.get('chat_history', [])

            # Generate response using the chat history and user input
            response = self.chain.invoke({
                "input": user_input,
                "chat_history": chat_history
            })

            # Update session chat history
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": response})
            session['chat_history'] = chat_history

            return response

        except Exception as e:
            logger.error(f"Error during chat: {e}")
            return "I encountered an error. Please try again."

    def clear_memory(self, session):
        """Clears the chat history stored in the session."""
        if 'chat_history' in session:
            session['chat_history'] = []
            logger.info("Chat history cleared from session.")
        else:
            logger.warning("No chat history found in session.")
