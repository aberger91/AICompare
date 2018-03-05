import glob
from scipy.io import arff
from nltk.stem import WordNetLemmatizer

STOPWORDS_PATH = 'books/stopwords.txt'
PUNCTUATION = ['"', ':', ',', '.', '!', '?', ';', '(', ')', '\'s', '\'']
STOPWORDS = open(STOPWORDS_PATH).read().strip('\n').split('\n\n')

lemmatizer = WordNetLemmatizer()

def get_files():
    text_files = glob.glob('books/*.txt')
    files = { }
    for f in text_files:
        key = f.replace('.txt', '')
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
    lemma_word = lemmatizer.lemmatize(word)
    if word in STOPWORDS:
        return li
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

def make_arff_meta(name, files, attributes, samples=250):
    file_ = '@relation %s\n\n' % name
    file_ += '@attribute %s {' % name
    for title, book in files.items():
        file_ += title + ', '

    file_ = file_.strip(', ')
    file_ += '}\n\n'
    for word, _ in attributes:
        file_ += '@attribute ' + word + ' numeric\n'#' {0, 1}\n'
    return file_

def make_arff(dest_path, n=250):
    def make_arff_data_row(title, paragraph, dict_):
        record = '%s,' % title
        for name, count in dict_:

            if name in paragraph:
                record += '1,'
            else:
                record += '0,'
        record = record.strip(',')
        return record

    files = get_files()
    word_counts = get_word_counts(files)

    sorted_dict = sorted(word_counts.items(), key=lambda x: x[1])
    sampled_sorted_dict = sorted_dict[-(n-1):]
    file_ = make_arff_meta('_author_', files, sampled_sorted_dict, samples=n)

    file_ += '''\n@data\n'''
    for title, book in files.items():
        for paragraph in book:
            record = make_arff_data_row(title, paragraph, sampled_sorted_dict)
            file_ += record + '\n'
    return file_

def create_and_load_arff(dest_path, n=250):
    file_ = make_arff(dest_path, n=n)
    with open(dest_path, 'w') as f:
        f.write(file_)
    try:
        arff_file = arff.loadarff(dest_path)
    except Exception as e:
        raise Exception('could not create a valid arff file ')
    return arff_file


if __name__ == '__main__':
    #main()
    create_and_load_arff('data.arff')

