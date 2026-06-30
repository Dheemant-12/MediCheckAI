from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from pypdf import PdfReader

import faiss
import numpy as np
import os
import pickle

from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

router = APIRouter()

load_dotenv()

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

INDEX_FILE = "faiss_index.bin"
CHUNKS_FILE = "chunks.pkl"

vector_store = None
stored_chunks = []
conversation_memory = []

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv(
        "NVIDIA_API_KEY"
    )
)

try:

    vector_store = faiss.read_index(
        INDEX_FILE
    )

    with open(
        CHUNKS_FILE,
        "rb"
    ) as file:

        stored_chunks = pickle.load(
            file
        )

except Exception:

    vector_store = None
    stored_chunks = []


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
                i:i + chunk_size
            ]
        )

    return chunks
@router.post("/upload-pdf")
async def upload_pdf(

    file: UploadFile = File(...)

):

    global vector_store
    global stored_chunks

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

    if len(chunks) == 0:

        return {

            "message":
            "No text found in PDF"

        }

    embeddings = model.encode(
        chunks
    )

    new_vectors = np.array(
        embeddings
    ).astype(
        "float32"
    )

    if vector_store is None:

        vector_store = faiss.IndexFlatL2(
            new_vectors.shape[1]
        )

    vector_store.add(
        new_vectors
    )

    # Add new chunks without removing old ones
    stored_chunks.extend(
        chunks
    )

    # Save FAISS index
    faiss.write_index(

        vector_store,

        INDEX_FILE

    )

    # Save all chunks
    with open(

        CHUNKS_FILE,

        "wb"

    ) as file:

        pickle.dump(

            stored_chunks,

            file

        )

    return {

        "message":
        "PDF added successfully",

        "characters":
        len(text),

        "new_chunks":
        len(chunks),

        "total_chunks":
        len(stored_chunks)

    }


@router.post("/ask-pdf")
async def ask_pdf(

    data: dict

):

    global conversation_memory
    global vector_store
    global stored_chunks

    question = data.get(
        "question"
    )

    if not question:

        return {

            "answer":
            "No question provided"

        }

    if vector_store is None:

        return {

            "answer":
            "No PDF uploaded"

        }

    conversation_memory.append({

        "role": "user",

        "content": question

    })

    question_embedding = model.encode(

        [question]

    )

    distances, indices = vector_store.search(

        np.array(
            question_embedding
        ).astype(
            "float32"
        ),

        min(
            3,
            len(stored_chunks)
        )

    )

    retrieved_chunks = []

    for idx in indices[0]:

        if (
            idx >= 0 and
            idx < len(stored_chunks)
        ):

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
            "Answer only using the provided context. If the answer is not available, clearly say so."

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
        retrieved_chunks[0][:150] if retrieved_chunks else ""

    }