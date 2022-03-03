
from sklearn import *
import numpy as np
import re
import nltk
from navec import Navec
import matplotlib.pyplot as plt
import joblib
import warnings
warnings.simplefilter(action='ignore')

nltk.download("stopwords")
plt.style.use('ggplot')

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc
)

nav = Navec.load('models/emb_navec.tar')
m1 = joblib.load('prod_models/m1.joblib')
m2 = joblib.load('prod_models/m2.joblib')
m3 = joblib.load('prod_models/m3.joblib')

segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
stopwords = nltk.corpus.stopwords.words('russian')



def normalizer (text):
    words_only = re.sub('[^А-я]+',' ',text.lower())
    doc = Doc(words_only)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    clean_text = []
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
        if (token.lemma not in stopwords) & (len(set(token.lemma))>1):
            clean_text.append(token.lemma)
            
    return ' '.join(clean_text)


def get_sentence_vector(sentence_list):
    vectors = []
    for sentence in sentence_list:
        sent_vec = []
        for i in sentence.split():
            if i in nav:
                sent_vec.append(nav[i])
            else:
                sent_vec.append(nav['<unk>'])
        if sentence.strip() == '':
            sent_vec = [nav['<unk>']]
        vectors.append(np.mean(sent_vec,axis=0))
    return np.vstack(vectors)


def voting(sentences,func=np.max):
    sentences = [normalizer(txt) for txt in sentences]
    probs = []
    probs.append(m1.predict_proba(sentences)[:,1])
    probs.append(m2.predict_proba(get_sentence_vector(sentences))[:,1])
    probs.append(m3.predict_proba(get_sentence_vector(sentences))[:,1])
    return np.apply_over_axes(func,np.array(probs),axes=0)[0]


if __name__ == '__main__':

    txt = None
    while txt != 'q':
        txt = input(f"Input some toxic or not very text\n")
        print('*'*50)
        print(f'{txt} is {voting([txt])[0]:.1%} toxic')