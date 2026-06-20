from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from pypdf import PdfReader

router = APIRouter()

knowledge_base = []


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

    knowledge_base.append(
        text
    )

    return {

        "message":
        "PDF uploaded successfully",

        "characters":
        len(text)

    }
