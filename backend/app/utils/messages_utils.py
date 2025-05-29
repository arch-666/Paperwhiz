from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def build_dynamic_chat_prompt(system_prompt: str, history: list, question: str):
    """
    Builds a ChatPromptValue using a dynamic system prompt, history, and new user question.
    
    Parameters:
    - system_prompt: str — description of the assistant's role (e.g., "You are a math tutor.")
    - history: list of (role, content) tuples, e.g., [("human", "..."), ("ai", "...")]
    - question: str — the new user query

    Returns:
    - ChatPromptValue: LangChain prompt object with structured messages
    """

    # Define prompt with dynamic system message
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("history"),
        ("human", "{question}")
    ])

    # Convert tuple history into LangChain Message objects
    message_history = []
    for role, content in history:
        if role == "human":
            message_history.append(HumanMessage(content=content))
        elif role == "ai":
            message_history.append(AIMessage(content=content))
        else:
            raise ValueError(f"Unknown role in history: {role}")

    # Inject values into the prompt
    return prompt.invoke({
        "history": message_history,
        "question": question
    })
