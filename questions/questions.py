import nltk
import sys
import string
import os
import math
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}

    for filename in os.listdir(directory):
        with open(os.path.join(directory,filename)) as f:
            files[filename] = f.read()

    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    final_list = []
    word_list = word_tokenize(document.lower())
    for word in word_list:
        if word in nltk.corpus.stopwords.words("english"):
            pass
        else:
            temp = False
            for c in word:
                if c not in string.punctuation:
                    temp = True
            if temp:
                final_list.append(word)

    return final_list
 
    
def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_idfs = {}

    for document in documents:
        for word in documents[document]:
            if word in word_idfs:
                pass
            else:
                counter = 0
                for document in documents:
                    if word in documents[document]:
                        counter += 1
                word_idfs[word] = math.log(len(documents)/counter)
        
    return word_idfs




def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    filenames = {}

    for word in query:
        word.lower()

    for file in files:
        filenames[file] = 0
        counter = 0
        for word in query:
            for file_word in files[file]:
                if word == file_word:
                    counter += 1
            filenames[file] += counter * idfs[word]
    
    ranked_filenames = [k for k, v in sorted(filenames.items(), key=lambda item: item[1], reverse=True)]
    temp = []
    for i in range(n):
        temp.append(ranked_filenames[i])
    return temp    
        

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    dict_sentences = {}

    for word in query:
        word.lower()

    for sentence in sentences:
        idfs_sum = 0
        word_count = 0
        for word in query:
            for sentence_word in sentences[sentence]:
                if sentence_word == word:     
                    idfs_sum += idfs[word]
                    word_count += 1
        qtd = word_count/len(sentences[sentence])
        dict_sentences[sentence] = [idfs_sum, qtd]
        
    
    ranked_sentences = [k for k, v in sorted(dict_sentences.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True)]
    temp = []
    for i in range(n):
        temp.append(ranked_sentences[i])
    return temp  


if __name__ == "__main__":
    main()
