# import logging
# from langchain.chains import RetrievalQA
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain
# from langchain.llms import HuggingFaceHub

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# class QueryEngine:
#     def __init__(self, vector_store=None, repo_id="google/flan-t5-base"):
#         self.vector_store = vector_store
#         self.repo_id = repo_id
#         self.llm = None
#         self.memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
#         self.chain = None
        
#         # Initialize LLM
#         self._initialize_llm()
    
#     def _initialize_llm(self):
#         """Initialize the language model"""
#         logging.info(f"Initializing language model: {self.repo_id}")
#         try:
#             self.llm = HuggingFaceHub(
#                 repo_id=self.repo_id,
#                 model_kwargs={"temperature": 0.5, "max_length": 512}
#             )
#             logging.info("Language model initialized successfully")
#         except Exception as e:
#             logging.error(f"Error initializing language model: {str(e)}")
#             raise
    
#     def set_vector_store(self, vector_store):
#         """Set or update the vector store"""
#         self.vector_store = vector_store
#         # Reset the chain since vector store has changed
#         self.chain = None
    
#     def get_conversation_chain(self):
#         """Get or create the conversation chain"""
#         if not self.vector_store:
#             logging.error("No vector store available. Set a vector store first.")
#             return None
        
#         if not self.chain:
#             logging.info("Creating conversation chain")
#             try:
#                 self.chain = ConversationalRetrievalChain.from_llm(
#                     llm=self.llm,
#                     retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
#                     memory=self.memory,
#                     return_source_documents=True
#                 )
#                 logging.info("Conversation chain created successfully")
#             except Exception as e:
#                 logging.error(f"Error creating conversation chain: {str(e)}")
#                 return None
        
#         return self.chain
    
#     def query(self, question):
#         """Query the documents with a natural language question"""
#         chain = self.get_conversation_chain()
#         if not chain:
#             return {
#                 "answer": "I'm sorry, but I'm not able to answer questions right now. Please ensure documents are indexed.",
#                 "source_documents": []
#             }
        
#         logging.info(f"Processing query: {question}")
#         try:
#             # Get response from chain
#             response = chain({"question": question})
            
#             # Extract answer and source documents
#             answer = response.get("answer", "I couldn't find an answer to that question.")
#             source_documents = response.get("source_documents", [])
            
#             # Extract unique sources
#             sources = []
#             for doc in source_documents:
#                 if hasattr(doc, 'metadata') and doc.metadata:
#                     if doc.metadata not in sources:
#                         sources.append(doc.metadata)
            
#             return {
#                 "answer": answer,
#                 "source_documents": sources
#             }
#         except Exception as e:
#             logging.error(f"Error querying documents: {str(e)}")
#             return {
#                 "answer": f"An error occurred while processing your question: {str(e)}",
#                 "source_documents": []
#             }
    
#     def reset_memory(self):
#         """Reset the conversation memory"""
#         self.memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
#         # Reset the chain to use the new memory
#         self.chain = None
#         logging.info("Conversation memory reset")



import nltk
import logging
import string
import re
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources (first-time only)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

logging.basicConfig(level=logging.INFO)

class QueryEngine:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Tokenize words
        words = word_tokenize(text)
        # Remove stop words
        words = [word for word in words if word not in self.stop_words]
        return words
    
    def answer_query(self, document_path, question, document_text=None):
        """
        Generate an answer for the question based on document content
        This is a simplified version using keyword matching and sentence retrieval
        """
        try:
            # Get document text if not provided
            if not document_text:
                from document_processor import DocumentProcessor
                doc_processor = DocumentProcessor()
                document_text = doc_processor.extract_text_from_file(document_path)
                
            if not document_text:
                return "I couldn't extract text from that document."
                
            # Preprocess question and document
            question_words = set(self.preprocess_text(question))
            sentences = sent_tokenize(document_text)
            
            # Score sentences based on keyword matching
            sentence_scores = []
            for i, sentence in enumerate(sentences):
                words = set(self.preprocess_text(sentence))
                # Score is the count of matching words
                score = len(question_words.intersection(words))
                sentence_scores.append((score, i, sentence))
            
            # Sort by score
            sentence_scores.sort(reverse=True)
            
            # If no good matches, return a generic response
            if not sentence_scores or sentence_scores[0][0] == 0:
                return "I couldn't find a relevant answer in the document."
                
            # Take top 3 sentences to form the answer
            top_sentences = [s for _, _, s in sentence_scores[:3]]
            
            # Format the answer
            answer = " ".join(top_sentences)
            
            return answer
        except Exception as e:
            logging.error(f"Error answering query: {e}")
            return "I encountered an error while processing your question."