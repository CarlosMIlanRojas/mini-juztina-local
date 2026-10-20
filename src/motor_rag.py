from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def inicializar_llm():
    return ChatOllama(model="qwen2.5", temperature=0.0)

def crear_prompt_estricto():
    """Usa ChatPromptTemplate para que Qwen respete las reglas del Sistema."""
    system_template = """Eres Mini_Juztina, un asistente legal estricto.
REGLAS INQUEBRANTABLES:
1. NO hagas resúmenes. NO expliques modificaciones.
2. Encuentra el artículo exacto que responde la pregunta, cópialo y DETENTE.
3. Si el artículo no está en los documentos, di: "No encontré el artículo exacto."."""
    
    human_template = """PREGUNTA: {question}

DOCUMENTOS RECUPERADOS (Busca solo aquí):
{context}

Copia el artículo exacto:"""
    
    return ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", human_template)
    ])

def configurar_asistente(retriever):
    llm = inicializar_llm()
    prompt = crear_prompt_estricto()
    
    def formatear_documentos(docs):
        return "\n\n---\n\n".join(doc.page_content for doc in docs)

    recuperador = RunnablePassthrough.assign(
        context=lambda x: retriever.invoke(x["question"])
    )

    cadena_generacion = (
        {
            "context": lambda x: formatear_documentos(x["context"]),
            "question": lambda x: x["question"]
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return recuperador | RunnablePassthrough.assign(answer=cadena_generacion)