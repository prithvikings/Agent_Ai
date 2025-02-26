import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PyMuPDFReader  # Correct PDF reader

def get_index(data, index_name):
    if not os.path.exists(index_name):
        print(f"Building index: {index_name}")
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index

# Load India PDF
pdf_path = os.path.join("data", "India.pdf")
pdf_reader = PyMuPDFReader()
india_pdf = pdf_reader.load_data([pdf_path])  # ✅ Pass file path as a list
india_index = get_index(india_pdf, "india")
india_engine = india_index.as_query_engine()
