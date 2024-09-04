import urllib.request
import re
import random
import xml.etree.ElementTree as ET
import os


def load_text_from_xml(file_path):
    """
    Load and concatenate text from an XML file.
    
    Args:
        file_path (str): The path to the XML file.
    
    Returns:
        str: The concatenated text of all excuses.
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract all the text within <text> tags under each <excuse>
    texts = []
    for excuse in root.findall('.//excuse'):
        text = excuse.find('text').text
        if text:
            texts.append(text.strip())
    
    # Join all extracted texts into a single string
    return ' '.join(texts)

def preprocess_text(text):
    """
    Preprocess the input text by converting it to lowercase and splitting it into words.

    Args:
        text (str): The raw text string.

    Returns:
        list: A list of lowercase words extracted from the text.
    """
    # Use regular expressions to split text into words based on non-alphabetic characters
    words = re.split(r'[^A-Za-z]+', text.lower())
    
    # Filter out any empty strings resulting from the split
    return list(filter(None, words))

def generate_ngram(words, n):
    """
    Generate an n-gram model from a list of words.

    Args:
        words (list): The list of words from the text.
        n (int): The size of the n-gram (e.g., 2 for bigram, 3 for trigram).

    Returns:
        list: A sorted list of n-grams and their frequencies, sorted by descending frequency.
    """
    gram = {}
    
    # Ensure that n is within a reasonable range
    assert 0 < n < 100, "n must be between 1 and 100"
    
    # Iterate through the list of words to create n-grams
    for i in range(len(words) - (n - 1)):
        key = tuple(words[i:i + n])  # Create an n-gram tuple
        gram[key] = gram.get(key, 0) + 1  # Increment the frequency count
    
    # Sort the n-grams by frequency in descending order
    return sorted(gram.items(), key=lambda item: -item[1])

def weighted_choice(choices):
    """
    Make a weighted random choice from a list of (n-gram, frequency) tuples.

    Args:
        choices (list): A list of tuples where each tuple contains an n-gram and its frequency.

    Returns:
        tuple: The selected n-gram based on weighted probability.
    """
    # Calculate the total frequency sum
    total = sum(freq for _, freq in choices)
    
    # Generate a random number between 0 and the total frequency
    r = random.uniform(0, total)
    upto = 0
    
    # Iterate through the choices to find where the random number falls
    for choice, freq in choices:
        if upto + freq > r:
            return choice
        upto += freq

def generate_ngram_sentence(gram, start_words, length=80):
    """
    Generate a sentence using the n-gram model starting with a specific phrase.

    Args:
        gram (list): The n-gram model as a list of (n-gram, frequency) tuples.
        start_words (str): The starting words or phrase.
        length (int, optional): The desired length of the generated sentence. Defaults to 50.

    Returns:
        str: The generated sentence.
    """
    # Split the starting words into a list
    start_words = start_words.strip().lower().split()
    
    # to determine the size fo the ngrams
    n = len(gram[0][0])
    
    #initializing the sentence
    sentence = start_words[:]
    
    for _ in range(length - len(start_words)):
        # Get the last (n-1) words from the current sentence as the context
        current_context = tuple(sentence[-(n-1):])
        
        # Find all n-grams that match the current context
        choices = [element for element in gram if element[0][:len(current_context)] == current_context]
        
        # If no exact match is found, reduce the context size iteratively
        while not choices and len(current_context) > 1:
            current_context = current_context[1:]
            choices = [element for element in gram if element[0][:len(current_context)] == current_context]
        
        # If still no match is found break
        if not choices:
            break
        
        # Select the next word based on the weighted probability of matching n-grams
        next_word = weighted_choice(choices)[len(current_context)]
        sentence.append(next_word)
    
    # Combine the list of words into a single string sentence
    return ' '.join(sentence)


def main():
    """
    Main function to interact with the user, generate the n-gram model, and print the generated sentence.
    """
    #the file path to the xml file
    file_path = 'Excuses.xml'

    if not os.path.exists(file_path):
      print(f"Error: The file '{file_path}' does not exist.")
      return
    
    # Load the text from the XML file
    text = load_text_from_xml(file_path)
    
    # Preprocess the text to obtain a list of words
    words = preprocess_text(text)

    # Prompt the user to enter the starting word for sentence generation
    start_word = input("Enter the starting word (e.g., he, he was, etc.): ").strip().lower()
    
    # Prompt the user to enter the desired size of the n-gram
    try:
        ngram_size = int(input("Enter the size of the n-gram (e.g., 2 for bigram, 3 for trigram, etc.): "))
        if not (1 < ngram_size < 100):
            raise ValueError
    except ValueError:
        print("Invalid n-gram size. Please enter an integer between 2 and 99.")
        return

    # Generate the n-gram model based on the specified size
    ngram = generate_ngram(words, ngram_size)

    # Generate the sentence using the n-gram model
    print(f"\nGenerating a {ngram_size}-gram sentence starting with '{start_word}': \"", end="")
    sentence = generate_ngram_sentence(ngram, start_word, 20)
    print(sentence, "\"")

if __name__ == "__main__":
    main()
