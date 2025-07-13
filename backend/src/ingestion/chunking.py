from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

class Chunking:

    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_pdf(self, file_path: str):
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

        # Pass the list of Document objects directly
        chunks = splitter.split_documents(docs)
        return chunks

if __name__ == "__main__":
    chunking = Chunking()
    pdf_path = input("Enter the path to the PDF file: ")
    chunks = chunking.chunk_pdf(pdf_path)
    print(f"Total chunks created: {len(chunks)}")
    for i, chunk in enumerate(chunks[:5]):
        print(f"Chunk {i+1}:\n{chunk.page_content}\n{'-'*40}")
