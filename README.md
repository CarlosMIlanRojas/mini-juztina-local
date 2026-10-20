# ⚖️ Asistente Legal Inteligente (Sistema RAG Local)

Sistema interactivo de consulta y análisis legal para la **Constitución Política** y el **Código Penal**, utilizando un enfoque de **Generación Aumentada por Recuperación (RAG)** totalmente local y offline.

---

## 📌 Descripción del Proyecto

El proyecto permite realizar consultas sobre textos legales en lenguaje natural. El sistema recupera los artículos y fragmentos normativos más relevantes desde una base de datos vectorial local para alimentar al modelo de lenguaje (LLM), garantizando respuestas precisas, contextualizadas y fundamentadas sin alucinaciones.

### Arquitectura y Roles del Equipo

- **Data Engineer (Roberto Cahua Vasquez):** Ingesta, chunking basado en estructura legal (Títulos/Artículos) y generación de embeddings locales para la base de datos vectorial utilizando **ChromaDB**.
- **AI Engineer (Carlos Mian Rojas):** Configuración del modelo LLM offline en **Ollama (Llama 3)**, ingeniería de prompts con restricciones legales, guardrails y cadena RAG mediante **LangChain**.
- **Full-Stack Developer (Diego Laura Fuentes):** Desarrollo de la interfaz de usuario con **Streamlit**, gestión de historial de sesión, panel de transparencia de fuentes y documentación del proyecto.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.10+
- **Interfaz de Usuario (UI):** Streamlit
- **Modelos & LLM:** Ollama (Llama 3)
- **Framework RAG:** LangChain
- **Base de Datos Vectorial:** ChromaDB
- **Embeddings:** Sentence-Transformers (HuggingFace)

---

## 🚀 Guía de Instalación y Configuración

Sigue estos pasos para clonar y ejecutar el proyecto de manera 100% local en un entorno Windows.

### 1. Requisitos Previos

Asegúrate de contar con lo siguiente instalado en tu equipo:
- **Python 3.10** o superior.
- **Git** instalado.
- **Ollama** instalado y ejecutándose en segundo plano ([Descargar Ollama](https://ollama.com/)).

### 2. Clonar el Repositorio

Abre tu terminal (PowerShell o CMD) y ejecuta:
```bash
git clone https://github.com/CarlosMIlanRojas/mini-juztina-local.git
cd mini-juztina-local
```

### 3. Crear y Activar el Entorno Virtual

Es indispensable usar un entorno virtual para aislar las dependencias del proyecto.
```bash
python -m venv venv
.\venv\Scripts\activate
```
*(Nota: Si PowerShell bloquea la activación, ejecuta `Set-ExecutionPolicy Unrestricted -Scope Process` y vuelve a intentarlo).*

### 4. Instalar Dependencias

Con el entorno virtual activado `(venv)`, instala las librerías necesarias:
```bash
pip install -r requirements.txt
```

### 5. Descargar el Modelo Local

Abre una nueva terminal y descarga el modelo Llama 3 en Ollama (esto descargará aproximadamente 4.7 GB la primera vez):
```bash
ollama run llama3
```
*(Una vez descargado y en la línea de comandos interactiva de Ollama, puedes cerrarla o escribir `/bye`).*

### 6. Ejecución del Sistema

1. **Ingesta de datos (Solo la primera vez o al actualizar leyes):**
   *(Asegúrate de tener los textos legales en la carpeta correspondiente según la estructura del proyecto).*
   ```bash
   python src/ingesta.py
   ```
2. **Levantar la Interfaz Gráfica:**
   ```bash
   streamlit run src/app.py
   ```

El sistema abrirá automáticamente una ventana en tu navegador web (usualmente en `http://localhost:8501`) lista para recibir consultas legales de manera offline.