"""
LegalEase API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()


# Create generator object
generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=200
    )


class DocumentResponse(BaseModel):
    document_type: str
    generated_text: str


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):

    try:

        generated_text = generator.generate_document(
            document_type=request.document_type.strip(),
            parties=request.parties.strip(),
            terms=request.terms.strip(),
            dates=request.dates.strip(),
        )

        return DocumentResponse(
            document_type=request.document_type.strip(),
            generated_text=generated_text,
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        ) from error