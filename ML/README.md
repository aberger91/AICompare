__| Andrew Berger | CS480 | HW5 | 3/6/2018 |__

# Bernoulli Naive Bayes Classification for Predicting the Authorship of Text

### Proposal

      This paper is a study in the classification of text by author using a naive bayesian bernoulli supervised learning model.
      The features of the model are the most frequent 1000 lemmatized words of all texts.
      The learning machine consumes arrays of 0s and 1s, each number representing whether or not the paragraph
      contains that particular feature. This program is able to predict authorship, given the occurance
      of textual features.

### Data and Feature Selection

      The text consumed by the classifier are non-fiction novels written between 1839 and 1884 from various American and English authors.
      Each row of data in the training set represents the occurance (or non-occurance) of commonly used words from all books per paragraph of text.
      The amount of data read from each novel is at least greater than 324 KB and not more than 759 KB.
      Stopwords are omitted as features and words are lemmatized before becoming a feature. 
      Lemmatization is used to reduce redundancy in the feature set and omit variants of stopwords.
      The number of features was optimized and chosen based on the best performance of a grid search, using values 100, 500, 1000, and 2500.

### Creation of Training Set

      The make_arff.py program reads 7 texts, each by different authors, generates a histogram of word counts, and writes the training data to a file.
      The most frequently occuring 1000 words are used to construct an arff file that can be read by the classify.py program.
      The data is generated as such: for each paragraph in a text, iterate through the 1000 words and
      write a 1 if the word occurs in the paragraph, otherwise write a 0. The first element of each record in the arff file is the author and is used
      to correctly identify the record during the training stage.
      Each of the 1000 words are declared as an attribute in the arff file, with possible values either 0 or 1.
      All paragraphs in the text are preprocessed to exclude stopwords and individual words are lemmatized down to their root form. The lemmatization
      process is conducted with the free and publicly available database called WordNet, via the python package "nltk" (Natural Language Toolkit).
      Training and test samples are split such that the model is trained on 9/10 of the data and tested on the remaining 1/10. 

### Execution

      Cross validation is used before execution to find the optimal parameters for alpha, the smoothing factor input into the Bayiasian algorithm. 
      In this study, Laplace smoothing is used to prevent certain features from obfuscating the calcuation of the posterior probability.
      Since even some of the most common 1000 words of all texts may not occur in a particular text, the probability of that feature would drop to zero without Laplace smoothing. 
      To prevent this effect, these features are given a very small value of alpha instead of zero. The value to use for alpha is discovered through a cross validated grid search.

### Evaluation


![Classification Report](data/results.png)

![Confusion Matrix](data/confusion.png)

