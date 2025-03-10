from transformers import pipeline

# Load Hugging Face Summarization Model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize_text(text, min_length=50, max_length=150):
    """Summarizes the given document text separately."""

    try:
        if not text or not text.strip():
            return {"error": "Text cannot be empty."}

        # Ensure input is long enough for summarization
        if len(text.split()) < 50:  # BART requires longer input
            return {"error": "Text is too short to summarize effectively."}

        # Summarize text
        summary = summarizer(text, min_length=min_length, max_length=max_length, do_sample=False)

        return summary[0]["summary_text"]

    except Exception as e:
        return {"error": f"Summarization failed: {str(e)}"}
