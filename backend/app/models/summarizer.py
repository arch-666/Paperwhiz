from langchain_huggingface import HuggingFacePipeline
#from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
import sys, os
sys.path.append(os.path.abspath("."))  # Add root (where 'app' is) to path

# Import your modular utilities
from utils.prompt_utils import get_summarization_prompt
from utils.model_utils import load_hf_pipeline

def load_summarizer_model(model_name="facebook/bart-large-cnn", model_length=120):
    """
    Loads a summarization pipeline and integrates it with a LangChain-compatible prompt chain.
    Uses modular helpers for prompt formatting and HF pipeline loading.
    """
    
    # Load the summarization pipeline via utility
    summarization_pipe = load_hf_pipeline(task="summarization", model_name=model_name, max_new_tokens=model_length)
    summarizer = HuggingFacePipeline(pipeline=summarization_pipe)
    
    # Output parser
    #parser = StrOutputParser()

    # Prompt formatter as a Lambda step
    prompt_fn = RunnableLambda(
        lambda inputs: get_summarization_prompt(
            inputs["text"] if isinstance(inputs, dict) and "text" in inputs else str(inputs)
        )
    )

    # Chain: format prompt → run model → parse output
    summarization_chain = prompt_fn | summarizer #| parser

    return summarization_chain
