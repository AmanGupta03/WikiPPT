from gensim.summarization.summarizer import summarize 
from gensim.summarization.summarizer import summarize_corpus
from gensim.summarization import keywords
import spacy
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

nlp = spacy.load("en_core_web_sm")

sentences_per_slide  = 5
words_per_slide = 150

def no_of_sentences(text):
    return len(sent_tokenize(text))

def extract_intro(text):
    return sent_tokenize(text)[0]
    # text = summarize(text, word_count=100, split=True)
    # return text[:min(5, len(text))]

def filter(content):
    res = []
    for data in content:
        if data['title'] == '' and data['desc'] == '':
            continue
        else:
            res.append(data)
    return res


def points_count(sen_count, total):
    nos = sum(sen_count)
    for i in range(len(sen_count)):
        sen_count[i] = sen_count[i] * (total/nos)
        if(sen_count[i] > 0):
            sen_count[i] = max(1, round(sen_count[i]))
        else:
            sen_count[i] = int(sen_count[i]);
    return sen_count

def summary(text, req):
    text = summarize(text, word_count = req * words_per_slide, split=True)
    text = text[:min(req, len(text))]
    return text


def bullets(content, slide_per_head):
    content = filter(content)
    sen_count = []
    req_points = []
   
    for data in content:
        cnt = no_of_sentences(data['desc'])
        sen_count.append(cnt)
        req_points.append(cnt)
   
    points_count(req_points, slide_per_head*sentences_per_slide) 
   
    for i in range(len(content)):
        text = content[i]['desc']
        if(sen_count[i] > req_points[i] and sen_count[i] > 1):
            text = summary(text, req_points[i])
        else:
            text = sent_tokenize(text)
        content[i]['desc'] = text

    return content

