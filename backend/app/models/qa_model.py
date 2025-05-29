from utils.model_utils import load_hf_pipeline
from langchain_huggingface import HuggingFacePipeline
#from langchain.output_parsers.string import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableLambda
from transformers.pipelines import pipeline

# Reuse the custom dynamic prompt function
from utils.messages_utils import build_dynamic_chat_prompt  # ← import this function

def load_qa_model(system_prompt="You are a helpful assistant."):
    """
    Loads a text-generation model (gpt2) wrapped with a dynamic chat prompt and output parser.
    Supports injecting dynamic system roles and history.
    """

    # Load Hugging Face pipeline
    pipe = load_hf_pipeline(task='text-generation', model_name="gpt2")
    llm = HuggingFacePipeline(pipeline=pipe)

    # Parser for extracting string output
    #parser = StrOutputParser()

    # Define the full QA chain using a lambda that builds prompts dynamically
    def format_inputs(inputs):
        """ inputs: dict with keys 'context', 'question', 'history' """
        context = inputs.get("context", "")
        question = inputs.get("question", "")
        history = inputs.get("history", [])

        # Inject context into question so model can answer with context
        full_question = f"Answer the following question based on the given content:\n\nContext: {context}\nQuestion: {question}"

        # Build a full LangChain prompt with role and memory
        prompt = build_dynamic_chat_prompt(system_prompt, history, full_question)

        return {"messages": prompt.to_messages()}

    chain = (
        RunnableLambda(format_inputs)
        | llm
      #  | parser
    )

    return chain
