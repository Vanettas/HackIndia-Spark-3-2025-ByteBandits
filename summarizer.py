from transformers import pipeline

# Load Hugging Face Summarization Model (BART or T5)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_text(text, min_length=50, max_length=150):
    """Summarizes the given document text using an NLP model."""
    if not text.strip():
        return {"error": "Text cannot be empty"}

    summary = summarizer(text, min_length=min_length, max_length=max_length, do_sample=False)

    return summary[0]["summary_text"]
