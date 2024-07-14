import nltk

nltk.download('punkt')

def split_script_into_sentences(script):
    return nltk.sent_tokenize(script)

# Example usage for testing
if __name__ == "__main__":
    script_text = ("""Artificial Intelligence (AI) is a broad branch of computer science that focuses on creating machines that can mimic human intelligence and perform complex tasks. AI enables computers to utilise advanced functions such as understanding spoken and written language, analysing data, making recommendations, and more.

One example of how AI is used is in optical character recognition (OCR). OCR uses AI to extract text and data from images and documents, turning unstructured content into structured data, and unlocking valuable insights. This is possible because AI can see and understand the text within images and documents, just like humans. This is accomplished with technologies like Convolutional Neural Networks (CNNs), and Recurrent Neural Networks (RNNs) which are modelled on the human brain and nervous system.

There are several applications of AI including agriculture, astronomy, governance, and many more. In agriculture, AI helps optimise various farming practices by analysing data and forecasting trends. In astronomy, AI enables scientists to analyse significant amounts of data, helping to discover new scientific insights.

AI can also be used for more sinister purposes. AI is exploited by authoritarian governments to control their citizens through facial and voice recognition techniques, enabling surveillance. This form of AI is also used to classify individuals as potential enemies of the state, targeting them with propaganda and misinformation.

Overall, AI is a set of technologies that allow computers to perform a variety of advanced functions, demonstrating intelligent behaviour to maximise the chances of achieving defined goals.

Remember, AI is all around us, from the personalised recommendations on Netflix to the interactive conversations with Google Assistant. Exciting advancements in AI are happening daily, and the future of this technology is limitless.""" )

    segments = split_script_into_sentences(script_text)
    for idx, segment in enumerate(segments):
        print(f"Segment {idx+1}: {segment}")
