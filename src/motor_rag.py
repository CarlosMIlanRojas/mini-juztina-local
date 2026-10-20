from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def inicializar_llm():
    return ChatOllama(model="qwen2.5", temperature=0.0)

def crear_prompt_estricto():
    """Prompt blindado con reglas inquebrantables extremas contra alucinaciones."""
    system_template = """Eres Mini_Juztina, un asistente legal estricto. 

REGLAS INQUEBRANTABLES:
1. LEE ÚNICAMENTE LOS DOCUMENTOS RECUPERADOS. Ignora por completo tu memoria o entrenamiento previo.
2. NO hagas resúmenes. NO expliques modificaciones ni des opiniones.
3. Verifica que el artículo recuperado trate EXACTAMENTE sobre el tema de la pregunta. 
4. Si encuentras el artículo correcto, CÓPIALO LITERALMENTE, cita su número y DETENTE.
5. Si los documentos recuperados hablan de otros temas (ej. si te preguntan por "la vida" y el texto habla de "elecciones" o "votos"), tienes ESTRICTAMENTE PROHIBIDO usarlos.
6. Si la respuesta no está clara en los documentos, es OBLIGATORIO responder textualmente: "No encontré el artículo exacto sobre este tema en los documentos recuperados."
"""
    
    human_template = """PREGUNTA: {question}

DOCUMENTOS RECUPERADOS (Busca solo aquí):
{context}

Copia el artículo exacto o indica que no se encontró:"""
    
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