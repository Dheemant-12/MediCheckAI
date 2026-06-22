from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from pypdf import PdfReader
import faiss
import numpy as np

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
