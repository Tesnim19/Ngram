# N-gram Sentence Generator

This project implements an N-gram model for generating sentences based on a provided text corpus. The text corpus is loaded from an XML file, and users can generate sentences by specifying a starting word or phrase. The n-gram model can be customized by setting the desired n-gram size (e.g., bigram, trigram, etc.).

## Features

- Load text data from an XML file.
- Preprocess text by splitting it into words.
- Generate n-grams of any size.
- Create sentences based on a specified starting word or phrase.
- Customize the length of the generated sentence.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Tesnim19/Ngram.git
   cd Ngram
   ```

2. **Place the XML File:**

Ensure the Excuses.xml file is in the same directory as the script.

3. **Run Script:**
    ```bash
    python ngram.py
    ```

## Usage

1. **Specify the Starting Word/Phrase:**

Provide a word or phrase to start the sentence generation.

2. **Set the N-gram Size:**

Input the desired size of the n-gram (e.g., 2 for bigram, 3 for trigram).

3. **Generated Sentence:**

The script will generate and display a sentence based on the specified parameters.

## Note:
If choose to use the notebook instead, open it in colab and make sure the Excuses.xml file is in the content directory. Or you can put it elsewhere but make sure to update the file path in the script.
