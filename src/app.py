import time
import streamlit as st

# --- 1. IMPORTACIONES DEL BACKEND (Tu trabajo y el del Integrante 1) ---
from motor_rag import configurar_asistente
# Asumimos que el Integrante 1 creó una función para cargar ChromaDB:
from ingesta import obtener_retriever 

# --- 2. INICIALIZAR EL CEREBRO UNA SOLA VEZ ---
# Usamos @st.cache_resource para que el modelo no se recargue cada vez que el usuario escribe algo
@st.cache_resource
def iniciar_sistema_rag():
    retriever = obtener_retriever()
    cadena = configurar_asistente(retriever)
    return cadena

# Cargamos el motor
rag_chain = iniciar_sistema_rag()

# Configuración inicial de la página
st.set_page_config(
    page_title="Asistente Legal RAG - Constitución y Código Penal",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Funciones Principales y Conectores de Backend
# -----------------------------------------------------------------------------
def obtener_respuesta_rag(prompt: str):
    """
    Función puente que ahora SÍ conecta con el motor RAG local.
    """
    # 1. Le pasamos la pregunta a tu cerebro (motor_rag.py)
    respuesta_rag = rag_chain.invoke({"question": prompt})
    
    # 2. Extraemos el texto generado por Ollama
    respuesta_texto = respuesta_rag["answer"]
    
    # 3. Extraemos los artículos recuperados por ChromaDB
    documentos_recuperados = respuesta_rag["context"]
    
    sources = []
    # Convertimos los documentos de LangChain al formato que necesita la interfaz
    for doc in documentos_recuperados:
        sources.append({
            # Usamos .get() por si el Integrante 1 usó otros nombres en los metadatos
            "libro": doc.metadata.get("fuente", "Norma Legal"),
            "articulo": doc.metadata.get("articulo", "Art. S/N"),
            "texto": doc.page_content
        })
    
    return respuesta_texto, sources

def simular_stream(texto: str):
    """Simula la escritura en tiempo real de la respuesta del modelo."""
    for palabra in texto.split(" "):
        yield palabra + " "
        time.sleep(0.05)

        # -----------------------------------------------------------------------------

# Inicialización Segura del Estado de Sesión

# -----------------------------------------------------------------------------

if "messages" not in st.session_state:

  st.session_state.messages = []



# -----------------------------------------------------------------------------

# Barra Lateral (Sidebar) de Control

# -----------------------------------------------------------------------------

with st.sidebar:

  st.title("Panel de Control")

  st.markdown("---")

  

  st.subheader("⚙️ Estado del Sistema")

  st.success("🟢 Base Vectorial: Conectada")

  st.info("🤖 Modelo LLM: Ollama (Local)")

  

  st.markdown("---")

  

  st.subheader("📚 Marco Normativo")

  st.markdown("- 📜 Constitución Política")

  st.markdown("- ⚖️ Código Penal")

  

  st.markdown("---")

  

  # Botón seguro para limpiar el historial

  if st.button("🗑️ Limpiar Conversación", use_container_width=True):

    st.session_state.messages = []

    st.rerun()



# -----------------------------------------------------------------------------

# Interfaz Principal de Chat

# -----------------------------------------------------------------------------

st.title("⚖️ Asistente Legal Inteligente (RAG)")

st.caption("Sistema local de consulta normativa con respaldo de fuentes oficiales.")



# Renderizar el historial de mensajes de forma segura

for message in st.session_state.messages:

  role = message.get("role", "user")

  content = message.get("content", "")

  sources = message.get("sources", [])

  

  with st.chat_message(role):

    st.markdown(content)

    

    # Mostrar panel de fuentes si existen

    if sources:

      with st.expander("📄 Ver fuentes y fragmentos normativos recuperados"):

        for idx, src in enumerate(sources, 1):

          st.markdown(f"**[{idx}] {src.get('libro', '')} — {src.get('articulo', '')}**")

          st.info(f"\"{src.get('texto', '')}\"")



# Capturar nueva entrada del usuario

if prompt := st.chat_input("Escribe tu consulta legal aquí..."):

  

  # 1. Almacenar y mostrar pregunta del usuario

  st.session_state.messages.append({"role": "user", "content": prompt})

  with st.chat_message("user"):

    st.markdown(prompt)



  # 2. Generar respuesta del asistente

  with st.chat_message("assistant"):

    with st.spinner("Consultando la base vectorial y generando respuesta..."):

      

      # Obtener datos de la consulta

      respuesta_texto, fragmentos = obtener_respuesta_rag(prompt)

      

      # Mostrar respuesta progresiva

      respuesta_completa = st.write_stream(simular_stream(respuesta_texto))



      # Panel de transparencia interactivo

      with st.expander("📄 Ver fuentes y fragmentos normativos recuperados"):

        for idx, src in enumerate(fragmentos, 1):

          st.markdown(f"**[{idx}] {src['libro']} — {src['articulo']}**")

          st.info(f"\"{src['texto']}\"")



  # 3. Guardar en la sesión de forma segura

  st.session_state.messages.append({

    "role": "assistant",

    "content": respuesta_completa,

    "sources": fragmentos

  }) 