# ⚖️ Asistente Legal Inteligente (Sistema RAG Local)



Sistema interactivo de consulta y análisis legal para la **Constitución Política** y el **Código Penal**, utilizando un enfoque de **Generación Aumentada por Recuperación (RAG)** totalmente local y offline.



---



## 📌 Descripción del Proyecto



El proyecto permite realizar consultas sobre textos legales en lenguaje natural. El sistema recupera los artículos y fragmentos normativos más relevantes desde una base de datos vectorial local para alimentar al modelo de lenguaje (LLM), garantizando respuestas precisas, contextualizadas y fundamentadas sin alucinaciones.



### Arquitectura y Roles del Equipo



* **Data Engineer (Roberto Cahua Vasquez):** Ingesta, chunking basado en estructura legal (Títulos/Artículos) y generación de embeddings locales para la base de datos vectorial (ChromaDB / FAISS).

* **AI Engineer (Carlos Mian Rojas):** Configuración del modelo LLM offline en Ollama (Llama 3 / Qwen), ingeniería de prompts con restricciones legales, guardrails y cadena RAG (LangChain / LlamaIndex).

* **Full-Stack Developer (Diego Laura Fuentes):** Desarrollo de la interfaz de usuario con Streamlit, gestión de historial de sesión, panel de transparencia de fuentes y documentación del proyecto.



---



## 🛠️ Tecnologías Utilizadas



* **Lenguaje:** Python 3.10+

* **Interfaz de Usuario (UI):** Streamlit / Chainlit

* **Modelos & LLM:** Ollama (Llama 3 / Qwen en español)

* **Framework RAG:** LangChain / LlamaIndex

* **Base de Datos Vectorial:** ChromaDB / FAISS

* **Embeddings:** HuggingFace / BGE-small-es



---



## 🚀 Guía de Instalación y Configuración



Sigue estos pasos para clonar y ejecutar el proyecto de manera local.



### 1. Requisitos Previos



Asegúrate de contar con lo siguiente instalado en tu equipo:



* **Python 3.10** o superior.

* **Git** instalado.

* **Ollama** instalado y ejecutándose en segundo plano ([Descargar Ollama](https://ollama.com/)).



### 2. Clonar el Repositorio



```bash

git clone https://github.com/CarlosMIlanRojas/mini-juztina-local

cd mini-juztina-local

Escribir mensaje
