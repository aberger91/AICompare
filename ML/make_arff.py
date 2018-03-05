import glob
import pickle
from scipy.io import arff
from nltk.stem import WordNetLemmatizer
from nltk import download

STOPWORDS_PATH = 'books/stopwords.txt'
PUNCTUATION = ['"', ':', ',', '.', '!', '?', ';', '(', ')', '\'s', '\'']
STOPWORDS = open(STOPWORDS_PATH).read().strip('\n').split('\n\n')
WORDNET_LEMMATIZER = WordNetLemmatizer()

def lemmatize(s):
    return WORDNET_LEMMATIZER.lemmatize(s)

def get_files():
    text_files = glob.glob('books/*.txt')
    files = { }
    for f in text_files:
        key = f.split('\\')[-1]
        key = key.replace('.txt', '')
        if key != 'stopwords':
            data = open(f).read().split('\n\n') # split by paragraph
            files[key] = data
    return files

def check_stopword_add_(word, li):
    def remove_punctuation(word):
        if word.isalnum():
            return word
        for c in PUNCTUATION:
            if c in word:
                word = word.replace(c, '')
        return word
    word = remove_punctuation(word).lower()
    if word in STOPWORDS or word == '':
        return li
    lemmatized_word = lemmatize(word)
    #print('Lemmatizing: (%s) => (%s)' % (word, lemmatized_word), end='\r')
    if lemmatized_word in STOPWORDS:
        return li
    li += [ lemmatized_word ]
    return li

def remove_stopwords(paragraph):
    li = paragraph.replace('\n', ' ').split(' ')
    new_paragraph = [ ]
    for s in li:
        if '--' in s:  # could do this in separate pass
            words = s.split('--')
            for w in words:
                li = check_stopword_add_(w, new_paragraph)
            continue
        li = check_stopword_add_(s, new_paragraph)
    return ' '.join(new_paragraph)

def get_word_counts(files):
    counts = { }
    for title, book in files.items():
        for paragraph in book:
            parsed_paragraph = remove_stopwords(paragraph)
            for w in parsed_paragraph.split(' '):
                if w == '':
                    continue
                if w in counts:
                    counts[w] += 1
                else:
                    counts[w] = 1
    return counts

def make_arff_meta(name, files, attributes):
    print('Creating arff metadata ...')
    file_ = '@relation %s\n\n' % name
    print('Adding Relation: %s' % file_, end='\r')
    file_ += '@attribute %s {' % name
    for title, book in files.items():
        file_ += title + ', '
    file_ = file_.strip(', ')
    file_ += '}\n\n'
    for word, _ in attributes:
        s = '@attribute ' + word + ' {0, 1}\n'
        print('Adding Attribute: %s' % s, end='\r')
        file_ += s
    return file_

def get_sampled_sorted_word_list(files, n):
    word_counts = get_word_counts(files)
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1])
    sampled_sorted_words = sorted_words[-(n-1):]
    f = open('wordcount.pylist', 'wb')
    pickle.dump(sampled_sorted_words, f)
    return sampled_sorted_words

def make_arff(dest_path, n):
    def make_arff_data_row(title, paragraph, li):
        record = '%s,' % title
        for name, count in li:
            if name in paragraph:
                record += '1,'
            else:
                record += '0,'
        record = record.strip(',')
        return record

    files = get_files()

    print('Generating arff file with %d features' % n)
    sampled_sorted_words = get_sampled_sorted_word_list(files, n)
    file_ = make_arff_meta('_author_', files, sampled_sorted_words)

    file_ += '''\n@data\n'''
    for title, book in files.items():
        for paragraph in book:
            record = make_arff_data_row(title, paragraph, sampled_sorted_words)
            file_ += record + '\n'
    with open(dest_path, 'w') as f:
        f.write(file_)
    return file_

def load_arff(path):
    try:
        arff_file = arff.loadarff(path)
    except Exception as e:
        raise Exception('could not load a valid arff file ')
    return arff_file

def main(argc, argv):
    if argc < 2:
        print('usage: make_arff.py <int>')
        return
    else:
        n = argv[1]
    download('wordnet')
    arff_path = 'data.arff'
    make_arff(arff_path, int(n))
    load_arff(arff_path)

if __name__ == '__main__':
    import sys
    main(len(sys.argv), sys.argv)

