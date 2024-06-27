import os
import time
from langchain.vectorstores import FAISS
#from langchain.document_loaders import Document
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from openai.error import RateLimitError
from langchain.memory.buffer import ConversationBufferMemory
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from llama_index.readers.google import GoogleDriveReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

#os.environ["OPENAI_API_KEY"] = ""

class BusinessChatbot:
        chat_history = []

        def __init__(self, documents):
            self.qa = self.load_templates(documents)

        def retry_on_rate_limit(func):
            def wrapper(*args, **kwargs):
                while True:
                    try:
                        return func(*args, **kwargs)
                    except RateLimitError as e:
                        print(f"Rate limit error: {e}")
                        print("Waiting for 20 seconds before retrying...")
                        time.sleep(20)
            return wrapper

        @retry_on_rate_limit
        def load_templates(self, documents):
            data = []
            for document in documents:
                doc = Document(page_content=document.text)
                data.append(doc)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=650, chunk_overlap=8)
            data = text_splitter.split_documents(data)


            
            
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

            vectorstore = FAISS.from_documents(data, embedding=embeddings)

            memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
            
            def truncate_prompt(prompt: str, max_tokens: int) -> str:
                tokens = prompt.split()  # simple whitespace tokenization
                if len(tokens) > max_tokens:
                    tokens = tokens[:max_tokens]
                return ' '.join(tokens)


            prompt_text = """
            You are a business chatbot designed to assist users with their business-related tasks. Your primary objectives are twofold:

            1. Answer Questions about the Provided Documents:
            - Your first role is to provide accurate and relevant information in response to user queries about the documents provided.
            - If a user asks a question pertaining to a specific detail in the documents, your task is to extract the relevant information and provide a clear answer.
            - For example, if a user asks about the ownership structure or financial status of the company mentioned in the documents, you should respond with precise details.

            2. Generate New Proposals Based on User Requirements:
            - Your second role is to generate new proposals based on user-provided requirements and instructions.
            - You need to search the proposals from all the documents for your help and use them as your template.
            - Use user's given information and write for those headings only in a proper proposal format. 
            - When a user requests the generation of a new proposal, you should interpret their requirements thoroughly and create a comprehensive proposal that meets their needs.
            - Ensure to include all necessary sections such as introduction, objectives, target audience, strategies, budget allocation, and timeline, as per the user's specifications.
            - Additionally, consider any specific information provided by the user, such as company name, date, or other relevant details, and incorporate them appropriately into the proposal.

            Please perform both roles effectively to assist users effectively in their business-related endeavors. Your ability to understand and fulfill user requests accurately and efficiently is crucial for providing a satisfactory user experience.
            """
            max_prompt_tokens = 4096 - 256  # adjust 256 as per your requirement
            prompt_text = truncate_prompt(prompt_text, max_prompt_tokens)

            system_prompt_template = f"""
            {prompt_text}
            ----
            {{context}}
            ----
            """
            user_prompt_template = "Question:```{question}```"
            messages = [
                SystemMessagePromptTemplate.from_template(system_prompt_template),
                HumanMessagePromptTemplate.from_template(user_prompt_template)
            ]
            qa_prompt = ChatPromptTemplate.from_messages(messages)
            llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0, max_tokens=500)
            qa = ConversationalRetrievalChain.from_llm(
                llm=llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever(),
                memory=memory,
                combine_docs_chain_kwargs={'prompt': qa_prompt}
            )

            return qa

        @retry_on_rate_limit
        def convchain(self, query):
            if not query:
                return

            result = self.qa({"question": query, "chat_history": self.chat_history})
            self.chat_history.extend([(query, result["answer"])])
            return result['answer']

        def clr_history(self, count=0):
            self.chat_history = []



def run_chatbot():
    from .datapipeline import get_data
    documents = get_data()
    business_bot = BusinessChatbot(documents)
    #print(documents[0].text) 
    return business_bot


def get_response(document_info_query,business_bot):
    response_doc_info = business_bot.convchain(document_info_query)
    return response_doc_info


