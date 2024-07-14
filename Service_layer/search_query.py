import json
import random
from langchain_community.llms.cohere import Cohere
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

def load_api_keys(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data['api_keys']
    except FileNotFoundError:
        print("API keys file not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from the API keys file.")
        return []

def select_api_key(api_keys):
    if api_keys:
        return random.choice(api_keys)
    else:
        raise ValueError("No API keys available.")

def create_search_query(text):
    api_keys = load_api_keys('keys.json')
    selected_key = select_api_key(api_keys)

    # Initialize model
    llm = Cohere(cohere_api_key=selected_key,
                 model='command', temperature=0.7, max_tokens=150, stop=['\n\n'])

    # Create the template string
    template = """Instructions:
Generate a concise and accurate search query for the given text to retrieve relevant stock videos. 
Focus on extracting the main keywords or objects described in the text, keeping the query as short as possible while maintaining relevance. 
Avoid including introductory phrases, scene settings, or unnecessary dialogue. Ensure the query captures the essential elements of the text.

Example:
Text: Solar power is harnessed by using photovoltaic cells to convert sunlight into electricity. It is a clean and renewable source of energy that can be used in various applications, from residential to industrial settings.
Search Query: Solar Power Photovoltaic Cells

Text: The yellow dog lives a carefree life, enjoying sunny days and playing in the park with other dogs.
Search Query: Yellow Dog Playing Park

Text: Climate change is caused by an increase in greenhouse gases in the atmosphere, which trap heat, resulting in a warmer planet.
Search Query: Climate Change Greenhouse Gases Warming Planet

Text: A scientist conducting an experiment in a modern laboratory with advanced equipment.
Search Query: Scientist Experiment Modern Laboratory Equipment

Text: {text}
Search Query:"""

    # Create prompt
    prompt = PromptTemplate(template=template, input_variables=["text"])

    # Create and run the llm chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.run(text=text)

    # Process the response to remove any redundant prefixes
    search_query = response.strip().replace('Search Query:', '').strip()
    return search_query

def create_search_queries(script_segments):
    queries = [create_search_query(segment) for segment in script_segments]
    return queries

def test_create_search_queries():
    # Example script segments
    script_segments = [
    "Artificial Intelligence (AI) is a broad branch of computer science that focuses on creating machines that can mimic human intelligence and perform complex tasks.",
    "AI enables computers to utilise advanced functions such as understanding spoken and written language, analysing data, making recommendations, and more.",
    "One example of how AI is used is in optical character recognition (OCR)",
    "SOCR uses AI to extract text and data from images and documents, turning unstructured content into structured data, and unlocking valuable insights.",
    "This is possible because AI can see and understand the text within images and documents, just like humans.",
    "This is accomplished with technologies like Convolutional Neural Networks (CNNs), and Recurrent Neural Networks (RNNs) which are modelled on the human brain and nervous system. ",
    "There are several applications of AI including agriculture, astronomy, governance, and many more.",
   "In agriculture, AI helps optimise various farming practices by analysing data and forecasting trends.",
    "In astronomy, AI enables scientists to analyse significant amounts of data, helping to discover new scientific insights.",
    "AI can also be used for more sinister purposes.",
    "AI is exploited by authoritarian governments to control their citizens through facial and voice recognition techniques, enabling surveillance.",
    "This form of AI is also used to classify individuals as potential enemies of the state, targeting them with propaganda and misinformation.",
    "SOverall, AI is a set of technologies that allow computers to perform a variety of advanced functions, demonstrating intelligent behaviour to maximise the chances of achieving defined goals.",
    "Remember, AI is all around us, from the personalised recommendations on Netflix to the interactive conversations with Google Assistant.",
    "Exciting advancements in AI are happening daily, and the future of this technology is limitless."]

    # Create search queries for each segment
    search_queries = create_search_queries(script_segments)
    
    # Print the generated search queries
    print("\nGenerated Search Queries:")
    for i, query in enumerate(search_queries):
        print(f"Query {i+1}: {query}\n")

if __name__ == "__main__":
    test_create_search_queries()

