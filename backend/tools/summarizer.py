from transformers.pipelines import pipeline
def summarizer(text: str, max_length: int = 130, min_length: int = 30) -> str | dict:
    pipe = pipeline("summarization", model="facebook/bart-large-cnn",truncation=True)
    # text = text[:2000]  # simple truncation to avoid token limit errors
    result = pipe(text, max_length=max_length, min_length=min_length, do_sample=False)
    if result is None:
        return {"error": "Summarization failed."}
    if isinstance(result, list):
        result_list = result
    else:
        try:
            result_list = list(result)
        except TypeError:
            return {"error": "Summarization failed."}
    if not result_list or not isinstance(result_list[0], dict) or "summary_text" not in result_list[0]:
        return {"error": "Summarization failed."}
    summary = result_list[0]["summary_text"]
    if not summary.strip():
        return {"error": "Summary is empty."}
    return summary