from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

def process_query(query):
    llm = ChatOpenAI(api_key="key")
    response = llm.complete(prompt=query)
    return response 