from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'}
)

db = Chroma(
    persist_directory="./chroma_db_legal",
    embedding_function=embeddings,
    collection_name="leyes_peru"
)

# Probamos buscando algo del Código Penal
resultados = db.similarity_search("¿Cuál es la pena por homicidio simple?", k=2)

for i, doc in enumerate(resultados):
    print(f"\n--- Resultado {i+1} ---")
    print("Metadatos:", doc.metadata)
    print("Contenido:", doc.page_content[:300], "...")