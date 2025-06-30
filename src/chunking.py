from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def chunk_pdf(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Pass the list of Document objects directly
    chunks = splitter.split_documents(docs)
    return chunks

if __name__ == "__main__":
    pdf_path = input("Enter the path to the PDF file: ")
    chunks = chunk_pdf(pdf_path)
    print(f"Total chunks created: {len(chunks)}")
    for i, chunk in enumerate(chunks[:5]):
        print(f"Chunk {i+1}:\n{chunk}\n{'-'*40}")