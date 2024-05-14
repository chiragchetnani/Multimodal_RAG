from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def answer(question , context) : 

    llm = ChatCohere(cohere_api_key="yEknIO6c0in2vwLIkh6JJ9x1WKLke7LPGbfbaiwi")


    chunks = [
        context[index : index + 512]
        for index 
        in range(0 , len(context) , 512)
    ]
    embeddings = HuggingFaceEmbeddings(
        model_name = 'sentence-transformers/all-MiniLM-L6-v2'
    )

    vc = FAISS.from_texts(chunks , embedding = embeddings)
    similar_docs = vc.similarity_search(question)

    context = ' '.join([
        element.page_content
        for element 
        in similar_docs
    ])

    prompt = '''
    Answer the following question solely based on the context provided

    Context : {} 

    Question : {}

    '''

    message = [
        HumanMessage(
            content = prompt.format(context , question)
        )
    ]

    return llm.invoke(message).content