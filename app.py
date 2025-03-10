import streamlit as st
import os
import shutil
from document_processor import DocumentProcessor
from document_navigator import DocumentNavigator
from embeddings_manager import EmbeddingsManager
from query_engine import QueryEngine

# Initialize components
doc_processor = DocumentProcessor()
doc_navigator = DocumentNavigator()
embed_manager = EmbeddingsManager()
query_engine = QueryEngine()

# Streamlit UI setup
st.set_page_config(page_title="AI Document Assistant", page_icon="📄", layout="wide")
st.title("📄 AI Assistant for Document Search & Q&A")

# Create necessary directories if they don't exist
os.makedirs("data/documents", exist_ok=True)

# Sidebar - Document Navigation
st.sidebar.header("📂 Document Navigation")

# Tab layout for adding and searching documents
tab1, tab2 = st.tabs(["📤 Upload Documents", "🔍 Search & Ask"])

with tab1:
    st.header("Upload New Document")
    
    # File upload section
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "docx"])
    doc_name = st.text_input("Document Name (optional, leave blank to use filename)")
    doc_content = st.text_area("Or paste document content directly", height=300)
    
    if st.button("Add Document"):
        if uploaded_file:
            # Save uploaded file
            file_name = doc_name if doc_name else uploaded_file.name
            save_path = f"data/documents/{file_name}"
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ {file_name} uploaded successfully!")
        elif doc_content:
            # Save pasted content
            file_name = f"{doc_name if doc_name else 'document'}.txt"
            save_path = f"data/documents/{file_name}"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(doc_content)
            st.success(f"✅ {file_name} created successfully!")
        else:
            st.error("Please either upload a file or paste document content")

with tab2:
    st.header("Search Documents & Ask Questions")
    
    # Search query input
    query = st.text_input("🔍 Search for a document:")
    if query:
        with st.spinner("Searching across your system..."):
            # Search in both project and system documents
            project_docs = doc_navigator.get_document_list()
            system_docs = doc_navigator.search_system_documents(query)
            
            # Display search results
            if project_docs or system_docs:
                st.sidebar.success(f"✅ Found {len(project_docs)} project document(s) and {len(system_docs)} system document(s)!")
                
                # Display project documents
                if project_docs:
                    st.sidebar.subheader("📁 Project Documents")
                    for i, doc in enumerate(project_docs, 1):
                        st.sidebar.write(f"{i}. {doc}")
                
                # Display system documents with locations
                if system_docs:
                    st.sidebar.subheader("💻 System Documents")
                    for i, doc in enumerate(system_docs, 1):
                        st.sidebar.write(f"{i}. {doc['name']}")
                        st.sidebar.write(f"   📍 Location: {doc['location']}")
                
                # Document selection
                selected_doc = st.sidebar.selectbox(
                    "📑 Select a Document",
                    options=[f"Project: {doc}" for doc in project_docs] + 
                            [f"System: {doc['name']}" for doc in system_docs]
                )
                
                if selected_doc:
                    doc_type, doc_name = selected_doc.split(": ", 1)
                    
                    # Handle document based on type
                    if doc_type == "Project":
                        doc_path = f"data/documents/{doc_name}"
                    else:
                        # Find the matching system document
                        doc_info = next(doc for doc in system_docs if doc['name'] == doc_name)
                        doc_path = doc_info['path']
                    
                    st.subheader(f"📖 Selected Document: {doc_name}")
                    st.write(f"📍 Location: {os.path.dirname(doc_path)}")
                    
                    # Show document content preview
                    doc_text = doc_processor.extract_text_from_file(doc_path)
                    with st.expander("📜 Document Preview"):
                        st.text_area("Content", value=doc_text[:2000] + "..." if len(doc_text) > 2000 else doc_text, 
                                    height=250, disabled=True)
                    
                    # Option to copy system document to project
                    if doc_type == "System":
                        if st.button("📥 Copy to Project"):
                            new_path = f"data/documents/{doc_name}"
                            shutil.copy2(doc_path, new_path)
                            st.success(f"✅ Document copied to project successfully!")
                    
                    # Q&A Section
                    st.subheader("🗣️ Ask Questions")
                    user_question = st.text_input("Enter your question about this document:")
                    if user_question:
                        with st.spinner("Generating answer..."):
                            response = query_engine.answer_query(doc_path, user_question, doc_text)
                            st.write("💡 Answer:")
                            st.markdown(response)
            else:
                st.sidebar.error("❌ No relevant documents found.")

# Show existing project documents
docs = doc_navigator.get_document_list()
if docs:
    st.sidebar.subheader("📚 Project Documents")
    for doc in docs:
        st.sidebar.write(f"• {doc}")
else:
    st.sidebar.info("No documents in project. Please upload one!")