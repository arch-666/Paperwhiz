from langchain.prompts import PromptTemplate

def get_summarization_prompt(text: str) -> str:
    prompt = PromptTemplate(
        template="Summarize the following content:\n\n{text}",
        input_variables=["text"]
    )
    return prompt.format(text=text)

def get_qa_prompt(context: str, question: str) -> str:
    prompt = PromptTemplate(
        template="Context:\n{context}\n\nQuestion:\n{question}\n\nAnswer:",
        input_variables=["context", "question"]
    )
    return prompt.format(context=context, question=question)

def get_parallel_prompt(input1: str, input2: str) -> str:
    prompt = PromptTemplate(
        template="Process the following inputs independently:\nInput1: {input1}\nInput2: {input2}",
        input_variables=["input1", "input2"]
    )
    return prompt.format(input1=input1, input2=input2)

def get_conditional_prompt(input: str) -> str:
    prompt = PromptTemplate(
        template="Input: {input}\n"
                 "If input is a question, answer it. If it's a command, explain how to do it.",
        input_variables=["input"]
    )
    return prompt.format(input=input)

def get_translation_prompt(text: str, language: str) -> str:
    prompt = PromptTemplate(
        template="Translate this text to {language}:\n\n{text}",
        input_variables=["text", "language"]
    )
    return prompt.format(text=text, language=language)

def get_code_generation_prompt(language: str, description: str) -> str:
    prompt = PromptTemplate(
        template="Write a {language} function that does the following:\n\n{description}",
        input_variables=["language", "description"]
    )
    return prompt.format(language=language, description=description)
