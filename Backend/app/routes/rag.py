from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from pypdf import PdfReader
import faiss
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv
from sentence_transformers import (
    SentenceTransformer
)

router = APIRouter()

knowledge_base = []
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

vector_store = None

stored_chunks = []
conversation_memory = []
load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv(
        "NVIDIA_API_KEY"
    )
)
def chunk_text(

    text,
    chunk_size=500

):

    chunks = []

    for i in range(

        0,
        len(text),
        chunk_size

    ):

        chunks.append(

            text[
                i:i+chunk_size
            ]

        )

    return chunks

@router.post("/upload-pdf")
async def upload_pdf(

    file: UploadFile = File(...)

):

    reader = PdfReader(
        file.file
    )

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted

    chunks = chunk_text(
    text
    )

    embeddings = model.encode(
        chunks
    )

    global vector_store
    global stored_chunks

    dimension = len(
        embeddings[0]
    )

    vector_store = faiss.IndexFlatL2(
        dimension
    )

    vector_store.add(

        np.array(
            embeddings
        ).astype(
            "float32"
        )

    )

    stored_chunks = chunks

    return {

    "message":
    "PDF processed",

    "characters":
    len(text),

    "chunks":
    len(chunks)

}
@router.post("/ask-pdf")
async def ask_pdf(

    data: dict

):

    question = data.get(
        "question"
    )

    if not question:

        return {
            "answer":
            "No question provided"
        }

    conversation_memory.append({

        "role": "user",

        "content": question

    })

    if vector_store is None:

        return {
            "answer":
            "No PDF uploaded"
        }

    question_embedding = model.encode(
        [question]
    )

    distances, indices = (

        vector_store.search(

            np.array(
                question_embedding
            ).astype(
                "float32"
            ),

            3

        )

    )

    retrieved_chunks = []

    for idx in indices[0]:

        if idx < len(stored_chunks):

            retrieved_chunks.append(
                stored_chunks[idx]
            )

    context = "\n\n".join(
        retrieved_chunks
    )

    messages = [

        {
            "role": "system",
            "content":
            "Answer only from the provided context."
        }

    ]

    messages.extend(
        conversation_memory[-4:]
    )

    messages.append({

        "role": "user",

        "content":
        f"""
Context:

{context}

Question:

{question}
"""

    })

    response = client.chat.completions.create(

        model="meta/llama-3.1-70b-instruct",

        messages=messages,

        temperature=0.2,

        max_tokens=300

    )

    answer = (
        response
        .choices[0]
        .message.content
    )

    conversation_memory.append({

        "role": "assistant",

        "content": answer

    })

    return {

        "answer":
        answer,

        "chunks_used":
        len(retrieved_chunks),

        "source_preview":
        retrieved_chunks[0][:150]

    }