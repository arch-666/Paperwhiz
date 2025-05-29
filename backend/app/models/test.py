# test_summarization.py

import sys
import os

# Manually add the path to the root directory where 'app' is located
sys.path.append('D:/Paperwhiz/backend/app')  # Adjust the path to match your actual project structure

# Now you can import from 'app.models' and 'app.utils'
from models.summarizer import load_summarizer_model

def test_summarizer():
    summarizer_chain = load_summarizer_model(model_name="facebook/bart-large-cnn",model_length=120)

    input_text = (
    "Artificial intelligence (AI) is a field of computer science that aims to create systems capable "
    "of performing tasks that typically require human intelligence. These tasks include learning, reasoning, "
    "problem-solving, perception, and language understanding. AI has many practical applications, such as "
    "natural language processing, image recognition, autonomous vehicles, and recommendation systems. "
    
    "AI can be categorized into narrow AI, which is designed to perform a specific task, and general AI, "
    "which has the potential to perform any intellectual task that a human being can do. While narrow AI is "
    "already in use today, general AI remains a theoretical concept. The development of AI technologies relies "
    "heavily on large datasets, powerful computing resources, and advanced algorithms. Machine learning, deep "
    "learning, and reinforcement learning are some of the techniques that have enabled the rapid growth of AI. "
    
    "In recent years, AI has made significant strides in various domains. In natural language processing, models "
    "like OpenAI’s GPT-3 and Google’s BERT have shown impressive capabilities in text generation, translation, and "
    "summarization. In computer vision, deep learning algorithms have enabled computers to recognize and interpret "
    "images with high accuracy, leading to advancements in facial recognition, autonomous vehicles, and medical imaging. "
    
    "Reinforcement learning, a branch of AI that focuses on training agents through trial and error, has led to "
    "breakthroughs in robotics, game playing, and optimization problems. Despite these advancements, AI also raises "
    "several ethical and societal concerns. The potential for job displacement due to automation, the risk of algorithmic "
    "bias, and the threat of AI being used for malicious purposes are all challenges that need to be addressed. "
    
    "There is also the concern of privacy, as AI systems often rely on vast amounts of personal data to train models. "
    "As AI continues to evolve, it will be important for governments, organizations, and individuals to collaborate in "
    "ensuring that AI is developed and deployed responsibly and ethically. Looking ahead, the future of AI holds exciting "
    "possibilities. AI systems may become more capable of performing complex tasks, such as creative problem-solving, "
    "and may even surpass human performance in certain domains. However, achieving general AI remains a distant goal, "
    "and much work remains to be done before machines can truly replicate human intelligence. Nonetheless, AI is poised "
    "to play an increasingly important role in shaping the future of technology, business, healthcare, education, and many "
    "other sectors."
)


    # Run the chain
    summary = summarizer_chain.invoke({"text": input_text})

    # # Print the result
    print("📄 Original text:\n", input_text)
    print("\n✂️ Summary:\n", summary)

if __name__ == "__main__":
    test_summarizer()
