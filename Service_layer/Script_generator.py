import json
import random
from langchain_community.llms import Cohere  # Library for interacting with Cohere
from langchain_cohere import ChatCohere, CohereRagRetriever  # Classes to use Cohere models
from langchain_core.prompts import PromptTemplate  # Class to define prompt templates
from langchain.chains import LLMChain  # For creating complex workflows
from sentence_transformers import SentenceTransformer, util  # For semantic similarity scoring

# Function to load API keys from a JSON file
def load_keys(filepath):
    try:
        with open(filepath, 'r') as file:
            keys = json.load(file)
            return keys.get('api_keys', [])  # Retrieve API keys list or return an empty list if not found
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading API keys: {e}")
        return []

# Function to select a random API key from the list
def pick_api_key(keys):
    if not keys:
        raise ValueError("No API keys available.")  # Raise an error if no API keys are available
    return random.choice(keys)

# Function to estimate the number of tokens needed for the specified duration
def estimate_token_count(duration_minutes):
    tokens_per_minute = 150  # Average tokens per minute for a speaking rate of 150 words per minute
    return duration_minutes * tokens_per_minute

# Function to generate an educational script using AI
def generate_script(topic, explanation_level, target_age, creativity, humor, duration_minutes):
    # Load API keys and select one
    keys = load_keys('keys.json')
    api_key = pick_api_key(keys)

    # Estimate the token count needed for the specified duration
    max_tokens = estimate_token_count(duration_minutes)

    # Initialize the language model with the selected API key
    llm = ChatCohere(cohere_api_key=api_key, model='command', temperature=0.8, max_tokens=max_tokens)
    retriever = CohereRagRetriever(llm=llm, connectors=[{"id": "web-search"}])

    # Retrieve relevant documents for the given topic
    documents = retriever.get_relevant_documents(topic)
    
    # Use a pre-trained model for semantic similarity
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(topic, convert_to_tensor=True)
    
    # Score and rank documents based on semantic similarity
    scored_docs = []
    for doc in documents:
        doc_embedding = model.encode(doc.page_content, convert_to_tensor=True)
        score = util.pytorch_cos_sim(query_embedding, doc_embedding)
        scored_docs.append((score.item(), doc.page_content))

    # Sort documents by score in descending order
    scored_docs.sort(reverse=True, key=lambda x: x[0])
    
    # Select top 3 most relevant documents
    context = " ".join(doc[1] for doc in scored_docs[:3])
    
    # Define level of explanation based on the user's input
    levels = {
        'beginner': "Explain this in a simple and easy to understand way for beginners. Help them understand the intuition, logic, and importance of it.",
        'intermediate': "Explain the topic with a bit more complexity and depth, assuming the reader has some prior knowledge and understanding. The script must be very long and detailed.",
        'advanced': "Delve into intricate details of the topic and explain it in depth. The reader has a solid foundation and is familiar with the intermediate concepts. Include more technical language, mathematical formulas, or advanced examples to provide a comprehensive understanding of the topic. Be extremely detailed."
    }
    level_description = levels.get(explanation_level, levels['beginner'])  # Default to 'beginner' if level is not specified

    # Define creativity and humor levels based on user input
    creativity_note = "" if creativity < 4 else "Include creative analogies." if creativity < 7 else "Be highly creative with analogies."
    humor_note = "" if humor < 4 else "Add a bit of humor." if humor < 7 else "Make it funny with jokes."

    # Create the prompt template for the language model
    prompt_template = """Instructions:\nCreate an educational script for a self contained video about {topic} such that a {target_age} year old can understand. Explain the key concepts. {level_description} {creativity_note} {humor_note} It should be in first person. Focus on extracting and explaining key concepts directly from the provided context {context} 
    The script should be direct and informative, emphasizing clarity and conciseness. do not do any introductory phrases, closing statements, and theatrical elements. Engage the audience by directly referencing and explaining the key points from the context.
    .\n"""

    # Define input variables for the prompt template
    prompt = PromptTemplate(template=prompt_template, input_variables=["topic", "target_age", "level_description", "creativity_note", "humor_note", "context"])

    # Create an LLM chain with the prompt and the language model
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # Invoke the LLM chain with the input data to generate the script
    response = llm_chain.invoke({
        "topic": topic,
        "target_age": target_age,
        "level_description": level_description,
        "creativity_note": creativity_note,
        "humor_note": humor_note,
        "context": context
    })

    # Return the generated script text
    return response['text']

# Function to print the formatted script text
def display_script(script_text):
    print(script_text)

# Example usage:
if __name__ == "__main__":
    # Generate a script on the topic "Climate Change" for a beginner level, 15-year-old audience, with moderate creativity and high humor, for 2 minutes duration
    script = generate_script("artificial intelligence", "beginner", 15, 4, 2, 2)
    display_script(script)
