import chainlit as cl
from faiss_doc_store import initialize_documents, initialize_faiss_document_store, initialize_rag_pipeline
import os


# Load environment variables
openai_key = os.environ['OPENAI_API_KEY']
openai_key='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'

# Initialize documents
filepath = 'data/recipe_docs.csv'
if not os.path.isfile(filepath):        
       print("Data file data/recipe_docs.csv not found")
       
documents = initialize_documents(filepath)

# Initialize document store and retriever
document_store, retriever = initialize_faiss_document_store(documents=documents)

# Initialize pipeline
query_pipeline = initialize_rag_pipeline(retriever=retriever, openai_key=openai_key)


@cl.on_message
async def main(message: str):
    # Use pipeline to get a response
    output = query_pipeline.run(query=message)

    # Create Chainlit message with response
    response = output['answers'][0].answer
    msg = cl.Message(content=response)

    # Send message to the user
    await msg.send()
