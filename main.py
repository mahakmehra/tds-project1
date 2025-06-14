import traceback
import base64
import io

from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image
import pytesseract

try:
    print("🚀 Starting TDS Virtual TA...")

    from rag.retriever import Retriever
    from rag.generator import Generator
    from rag.config import settings

    app = FastAPI(title="TDS Virtual TA")

    print("✅ Initializing retriever and generator...")
    retriever = Retriever()
    generator = Generator()

    print("✅ Initialization complete")

    class QuestionRequest(BaseModel):
        question: str
        image: str | None = None

    @app.post("/api/")
    async def answer_question(request: QuestionRequest):
        print("📥 Received question:", request.question)

        contexts = retriever.retrieve_with_threshold(
            request.question,
            top_k=3,
            min_score=0.5
        )

        if request.image:
            try:
                print("🖼️ Processing image...")
                image_data = base64.b64decode(request.image)
                image = Image.open(io.BytesIO(image_data))
                extracted_text = pytesseract.image_to_string(image)
                print("📝 Extracted text from image:", extracted_text[:100])

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
                print("❌ Error in image processing:", str(e))
                traceback.print_exc()
                return {
                    "answer": f"❌ Failed to process image: {str(e)}",
                    "links": []
                }

        if not contexts:
            print("⚠️ No relevant context found.")
            return {
                "answer": "I couldn't find enough relevant information to answer this question.",
                "links": []
            }

        print("🧠 Generating response...")
        response = generator.generate_response(request.question, contexts)
        print("✅ Response generated")

        return {
            "answer": response["answer"],
            "links": response["sources"]
        }

    print("✅ App is ready to serve!")

except Exception as e:
    print("💥 Fatal error during startup:", str(e))
    traceback.print_exc()
