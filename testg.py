from rag.generator import Generator
from rag.config import settings

def test_generator():
    print("Testing generator with mock context...")
    generator = Generator()
    mock_context = [{
        "content": "For VS Code setup, install Python extension and configure settings...",
        "metadata": {
            "title": "VS Code Setup Guide",
            "url": "https://course.example.com/vscode",
            "source": "course_content"
        }
    }]
    response = generator.generate_response("How to setup VS Code?", mock_context)
    print("Generated response:")
    print(response["answer"])
    print("\nSources:")
    for src in response["sources"]:
        print(f"- {src['title']}: {src['url']}")

if __name__ == "__main__":
    test_generator()