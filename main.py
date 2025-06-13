from fastapi import FastAPI
from pydantic import BaseModel
from rag.retriever import Retriever
from rag.generator import Generator
from rag.config import settings
import pytesseract
from PIL import Image
import base64
import io

app = FastAPI(title="TDS Virtual TA")
retriever = Retriever()
generator = Generator()

class QuestionRequest(BaseModel):
    question: str
    image: str | None = None

# @app.post("/api/")
# async def answer_question(request: QuestionRequest):
#     # Retrieve relevant contexts
#     contexts = retriever.retrieve_with_threshold(
#         request.question,
#         top_k=3,
#         min_score=0.5
#     )
    
#     if not contexts:
#         return {
#             "answer": "I couldn't find enough relevant information to answer this question.",
#             "links": []
#         }
    
#     # Generate answer using LLM
#     response = generator.generate_response(request.question, contexts)
    
#     return {
#         "answer": response["answer"],
#         "links": response["sources"]
#     }

@app.post("/api/")
async def answer_question(request: QuestionRequest):
    contexts = retriever.retrieve_with_threshold(
        request.question,
        top_k=3,
        min_score=0.5
    )

    # ✅ Handle base64-encoded image if provided
    if request.image:
        try:
            image_data = base64.b64decode(request.image)
            image = Image.open(io.BytesIO(image_data))
            extracted_text = pytesseract.image_to_string(image)
            contexts.append({
                "content": extracted_text,
                "metadata": {
                    "source": "Image OCR",
                    "title": "Extracted from image",
                    "url": "N/A"
                },
                "score": 1.0
            })
        except Exception as e:
            return {
                "answer": f"❌ Failed to process image: {str(e)}",
                "links": []
            }

    if not contexts:
        return {
            "answer": "I couldn't find enough relevant information to answer this question.",
            "links": []
        }

    response = generator.generate_response(request.question, contexts)

    return {
        "answer": response["answer"],
        "links": response["sources"]
    }
