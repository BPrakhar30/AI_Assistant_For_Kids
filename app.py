import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import openai
import pandas as pd
from speech2text import SpeechToText 
from text2speech import generate_and_play_speech


# Loading environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

# Defining paths
csv_file_path = r"path/to/your/csv"
persist_directory = r"path/for/vectordb"
if not os.path.exists(persist_directory):
    os.mkdir(persist_directory)
    
# Loading CSV data and creating embeddings
def load_data_and_embeddings():
    loader = CSVLoader(file_path=csv_file_path)
    data = loader.load()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    db = FAISS.from_documents(data, embeddings)
    db.save_local(persist_directory)
    return db


db = load_data_and_embeddings()
retriever = db.as_retriever()

# Initializing the LLM and chain
llm = ChatOpenAI(model_name="gpt-4-turbo")
prompt = ChatPromptTemplate.from_template(""" You are meant to be a chatbot for children. Always be appropriate, polite, and friendly. Engage in a two-way interaction, never referring to the child in the third person.
Question: {input}
For every question you have to decide whether you should answer according to the context or the previous conversations you had with the kid. You will answer according to the context when the question will be clear but when the question is not clear you will answer according to the previous conversations. 
Below is the context, If you don't find relevant context, respond in a friendly and engaging manner to keep the conversation going. Do not hallucinate, stay accurate and be factual. Your generated text should only be the response to the question asked by the child and nothing else. Here is the 
context: {context}
Below is the last few conversations you had with the kid:
{history}
""")


document_chain = create_stuff_documents_chain(llm, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Function to handle the response generation and updating history and vector store
def handle_response(input_text):
    if input_text:
        # Getting the conversation history as a string
        history_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.conversation_history])
        print(f"Conversation History:\n{history_str}")

        response = retrieval_chain.invoke({"input": input_text, "history": history_str})
        answer = response['answer']
        # st.write(answer)

        # # Streaming the generated speech as the text is displayed
        # generate_and_stream_speech(answer, voice="Dan")

        # Generating and playing the speech
        generate_and_play_speech(answer, voice="Default")

        st.session_state.conversation_history.append({"role": "user", "content": input_text})
        st.session_state.conversation_history.append({"role": "assistant", "content": answer})

        if len(st.session_state.conversation_history) > 10:
            st.session_state.conversation_history = st.session_state.conversation_history[-10:]

        # Summarizing conversation
        combined_content = f"Child's response: {input_text}"
        final_response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in writing the important condensed points from a child's responses in a conversation. You have to only write the likes, dislikes of the child, his daily activities or any other attributes about the child which should be remembered by his soulmate chatbot. Only write details if the child mentions these things otherwise your response should be empty."},
                {"role": "user", "content": combined_content}
            ],
            temperature=0.6
        )
        final_summary = final_response.choices[0].message.content

        # Updating CSV file and vector store
        df = pd.read_csv(csv_file_path)
        df.at[0, 'interests'] = df.at[0, 'interests'] + final_summary if pd.notna(df.at[0, 'interests']) else final_summary
        df.to_csv(csv_file_path, index=False)

        db = load_data_and_embeddings()
        print("Vector store updated with new summary.")

# Streamlit UI
st.title("Your Soulmate")

input_text = st.text_input("Let's Talk")

if st.button("Record and Get Response"):
    stt = SpeechToText()
    audio_filename = "output.wav"
    st.write("Recording for 5 seconds...")
    transcription = stt.record_and_transcribe(filename=audio_filename, duration=5)
    st.write("You said:", transcription)
    handle_response(transcription)

if st.button("Type and Get Response") and input_text:
    handle_response(input_text)
