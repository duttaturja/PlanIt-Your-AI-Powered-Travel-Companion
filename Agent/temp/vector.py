from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationVectorStoreTokenBufferMemory
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TravelAgentVectorMemory:

    def __init__(self):
        # Initialize LLM and vector store
        self.llm = OllamaLLM(model="llama3.2:1b")
        embedding_model = OpenAIEmbeddings()  # Replace with your embedding model
        self.vector_store = FAISS.load_local("faiss_index", embedding_model)
        self.memory = ConversationVectorStoreTokenBufferMemory(
            llm=self.llm,
            vectorstore=self.vector_store,
            memory_key="chat_history",
            max_token_limit=1000  # Adjust as needed
        )

        # Define the prompt
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

        # Create a processing chain
        self.chain = self.prompt | self.llm | StrOutputParser()

    def chat(self, user_input: str) -> str:
        logger.info(f"User: {user_input}")

        # Retrieve relevant chat history using vector search
        relevant_context = self.vector_store.similarity_search(user_input, k=5)
        chat_history = "\n".join([doc.page_content for doc in relevant_context])

        # Generate response
        response = self.chain.invoke({
            "input": user_input,
            "chat_history": chat_history
        })

        # Save context to memory
        self.memory.save_context({"input": user_input}, {"output": response})
        logger.info(f"Agent: {response}")
        return response

    def clear_history(self):
        self.memory.clear()
        logger.info("Vector memory cleared")
