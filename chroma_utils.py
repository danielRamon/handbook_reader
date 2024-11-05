from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

embed = OllamaEmbeddings(
    model="jina/jina-embeddings-v2-base-es")  # Initialize embeddings


def save_handbook_to_chroma(handbook_data: list) -> bool:
    """
    Saves the entire handbook data to Chroma with embeddings.

    Args:
        handbook_data (list): List of dictionaries containing title, URL, and text content of each section.

    Returns:
        bool: True if the handbook is saved correctly, False otherwise.
    """
    embeddings = OllamaEmbeddings(
        model="llama3.1",
    )

    documents = []
    for chapter in handbook_data:
        for section in chapter:
            document = Document(
                page_content=section.get('text', ''),
                metadata={
                    'title': section.get('title', ''),
                    'url': section.get('url', '')
                }
            )
            documents.append(document)
    print("Saving handbook to Chroma. This process can take a long time.")
    try:
        ids = [str(i) for i in range(1, len(documents) + 1)]
        Chroma.from_documents(
            documents=documents, embedding=embed, persist_directory="./chroma_data", ids=ids)
        return True
    except Exception as e:
        print(f"Error saving handbook to Chroma: {e}")
        return False


def ask_chroma(question: str, k: int = 3) -> dict:
    """
    Asks Chroma a question and returns the top k most similar results.

    Args:
        question (str): The question to ask Chroma.
        k (int): The number of most similar results to return. Default is 3.

    Returns:
        dict: A dictionary containing the top k most similar results.
    """
    try:
        vectorstore = Chroma(
            embedding_function=embed,  # Provide the embedding function
            persist_directory="./chroma_data"
        )
        results = vectorstore.similarity_search(question, k)
        return results
    except Exception as e:
        print(f"Error asking Chroma: {e}")
        return {}


# similars = ask_chroma(
#     "¿Quienes asisten al consejo de barrio?", 2)
# for similar in similars:
#     print(similar.page_content+"\n"*3)
