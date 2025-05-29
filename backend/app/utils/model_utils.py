from transformers.pipelines import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM, AutoModel
from typing import Optional, Union

def load_hf_pipeline(
    task: str,
    model_name: Optional[str] = None,
    tokenizer_name: Optional[str] = None,
    max_new_tokens: int = 150,
    device: int = -1  # -1 = CPU, 0 = first GPU
):
    """
    Load a Hugging Face pipeline for a specified task.

    Args:
        task (str): One of 'text-generation', 'summarization', 'question-answering', etc.
        model_name (str): HF model repo name. If None, defaults will be used.
        tokenizer_name (str): Tokenizer name. Defaults to model_name.
        max_new_tokens (int): For generation tasks.
        device (int): -1 for CPU, 0+ for GPU device ID.

    Returns:
        transformers.Pipeline
    """
    
    default_models = {
        "text-generation": "gpt2",
        "summarization": "facebook/bart-large-cnn",
        "question-answering": "distilbert-base-cased-distilled-squad",
        "translation": "Helsinki-NLP/opus-mt-en-de",
        "text-classification": "distilbert-base-uncased-finetuned-sst-2-english",
        "ner": "dslim/bert-base-NER",
        "embedding": "sentence-transformers/all-MiniLM-L6-v2"
    }

    if model_name is None:
        model_name = default_models.get(task)
        if not model_name:
            raise ValueError(f"No default model defined for task: {task}")

    if tokenizer_name is None:
        tokenizer_name = model_name

    # Choose model class based on task
    if task in ["summarization", "translation"]:
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    elif task in ["text-generation"]:
        model = AutoModelForCausalLM.from_pretrained(model_name)
    elif task in ["text-classification", "question-answering", "ner"]:
        model = AutoModel.from_pretrained(model_name)
    else:
        model = model_name  # some pipelines (like embeddings) can accept just model_name

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    pipe = pipeline(
        task=task,
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_new_tokens if "generation" in task or task in ["summarization", "translation"] else None,
        device=device
    )

    return pipe