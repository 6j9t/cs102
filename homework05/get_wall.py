from postredact import redact_finish, redact
from gensim.models.ldamulticore import LdaModel
from gensim.corpora.dictionary import Dictionary


def lda_mod(domains):
    common_texts = redact_finish(domains)
    common_dictionary = Dictionary(common_texts)
    common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]
    lda = LdaModel(common_corpus, num_topics=len(domains))
    return lda


def predict_topic(lda, text):
    predict_texts = [redact(text)]
    predict_dictionary = Dictionary(predict_texts)
    predict_corpus = [predict_dictionary.doc2bow(text) for text in predict_texts]
    unseen_doc = predict_corpus[0]
    vector = lda[unseen_doc]
    return vector


def topic(domain, text):
    max = 0
    cou = 0
    for a, b in predict_topic(lda_mod(domain), text):
        if b > max:
            max = b
            cou = a
    print(max, cou)
    return redact_finish(domain)[cou]

print(topic("-29591610","кроты"))
