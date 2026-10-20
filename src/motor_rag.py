from langchain_community.llms import Ollama
from langchain_coreprompts import PromptTemplate
from langchain_chains.combine_documents import create_stuff_documents_chain

def inicializar_llm():
    #Instanciamos el modelo local.
    llm = Ollama(model="llama3", temperature=0.1)
    return llm

def crear_promp_estricto():
    template = """
    Eres Mini_Juztina, un asistente legal estricto especializado EXCLUSIVAMENTE en la Constitución Politica del Perú y el Código Penal Peruano.

    REGLAS OBLIGATORIAS:
    1. Si la pregunta NO se trata sobe la Constitución Política del Perú o el Código Penal del Perú, responde EXACTAMENTE: "Lo siento, mi alcance se limita exclusivamente a consultas sobre la Constitución Política del Perú y el Código Penal Peruano. No puedo asesorar sobre esa materia."
    2. Basa tu respuesta ÚNICAMENTE en el contexto proporcionado abajo. NO uses conocimientos externos.
    3. NO inventes información, leyes, incisos o articulos.
    4. Cita SIEMPRE el nombre de la ley y el número del Articulo que sustenta tu respuesta.

    Contexto recuperado:
    {context}

    Pregunta: {input}
    Respuesta:
    """
    return PromptTemplate.from_template(template)

def configurar_asistencia(retriever):
    llm = inicializar_llm()
    prompt = crear_promp_estricto()

    # 1. Cadena de documentos: Emsambla el LLM con nuestras eglas (prompt)
    document_chain = create_stuff_documents_chain(llm, prompt)

    # 2. Cadena de recuperación: Conecta el buscador (retriever) con la cadena de documentos
    rag_chain = create_retrieval_chain(retriever, document_chain)

    return rag_chain