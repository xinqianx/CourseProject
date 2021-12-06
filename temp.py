from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
import os
import module
import requests
from bs4 import BeautifulSoup
import re
from nltk.probability import FreqDist
from nltk.util import ngrams
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS

ENGLISH_STOP_WORDS = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
app = Flask(__name__)

all_category = ['sports', 'food', 'travel', 'occupation', 'tv show', 
                'movie', 'video games', 'clothing brand', 'celebrities', 'company']

def decide_threshold(lens):
    if lens <=500:
        return 1
    if lens <= 1000:
        return 2
    if lens <= 2000:
        return 3
    if lens <= 3000:
        return 4
    if lens<=4000:
        return 5
    return 6

def find_top_match(user_input, threshold=1):
    top_word = []
    top_category = []
    top = dict((k, v) for k, v in user_input.items() if v > threshold)
    tb_ = module.Category()
    for category in all_category:
        category_ = tb_.getKeyWordByName(category)
        category_ = category_.split(',')
        processedCategory = []
        for cc in category_:
            tmp = cc.lower().split(' ')
            processedCategory += tmp
        for w in top:
            if w.lower() in processedCategory:
                top_word.append(w)
                top_category.append(category)

    return top_word, list(set(top_category))

def listToString(s): 
    str1 = " " 
    return (str1.join(s))

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def getURL(url):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    html = requests.get(url,headers=headers)
    bs_html = BeautifulSoup(html.text,'html.parser')

    #remove stopwords and single digit word
    words = [word for word in bs_html.text.split() if word.lower() not in ENGLISH_STOP_WORDS]
    rm_stopwords = " ".join(words)

    content = re.findall(r'\w+', rm_stopwords) #remove punctuation
    lens = len(content)
    #filter numbers
    def int_filter(list_i):
        for v in list_i:
            try:
                int(v)
                continue # Skip these
            except ValueError:
                yield v # Keep these

    number_filter = (list(int_filter(content)))

    len_filter = [w for w in number_filter if len(w)>1]

    data = {}
    #store in dictionary and word count
    for i in range(len(len_filter)):
        if len_filter[i].lower() not in data:
            data[len_filter[i].lower()] = 1 #lowercase only
        else:
            data[len_filter[i].lower()] += 1

    #sort in descending order
    sort_orders = sorted(data.items(), key=lambda x: x[1], reverse=True)
    sort_dict = {}
    for i  in sort_orders:
        sort_dict[i[0]] = i[1]

    return sort_dict,lens

@app.route('/insert_user')
def insert_user():
    name = request.args.get('name')
    categories = request.args.get('categories')
    feedback = request.args.get('feedback')
    tb = module.Users()
    result = tb.create(name,categories,feedback)
    return result

@app.route('/clear_all_user')
def drop_all_user():
    tb = module.Users()
    tb.dropTable()
    return "emptyUserTableNow"

##/update_user?name=zhengkai%20zhang&categories=Technology,Food,Entertainment&feedback=pokemon
@app.route('/update_user')
def update_user():
    name = request.args.get('name')
    categories = request.args.get('categories')
    feedback = request.args.get('feedback')
    tb = module.Users()
    return tb.updateUser(name,categories,feedback)

@app.route('/', methods=['GET','POST'])
def root():
    errors = []
    result = {}
    allUsers = []
    keyWords = []
    top3Key = []
    categoriesFind = []
    covered = []
    neu=''
    neg=''
    pos=''
    checked_= False
    tb = None
    tb_=None
    try:
        tb = module.Users()
        tb_ = module.Category()
        allUsers = tb.allUsers()
    except:
        errors.append('not able to fetch user db')
    if request.method == "POST":
        try:
            url = request.form['url']
            user = request.form['user']
            result = {
                'user': user,
                'url': url
            }
            urldata,lens = getURL(url)
            selectedUser = tb.getByName(user)
            feedback_ = str(selectedUser.feedback)
            keyWords = feedback_    .split(',')
            currentCategories = str(selectedUser.categories)
            currentCategories = currentCategories.split(',')
            all_text = listToString(list(urldata.keys()))
            sid_obj = SentimentIntensityAnalyzer()
            sentiment_dict = sid_obj.polarity_scores([all_text])
            neu = sentiment_dict['neu'] * 100
            neg = sentiment_dict['neg'] * 100
            pos = sentiment_dict['pos'] * 100
            threshold = decide_threshold(lens)
            topWords,categoriesFind = find_top_match(urldata, threshold)
            for c in currentCategories:
                k = tb_.getKeyWordByName(c)
                keyWords.append(k)
            proccessedKeywords = []
            for kk in keyWords:
                tmp = kk.lower().split(' ')
                proccessedKeywords += tmp
            covered = intersection(topWords,proccessedKeywords)
            top3Key = topWords[0:3]
            if len(covered) >= 1:
                checked_ = True
            else:
                checked_ = False
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('index.html', errors=errors, result=result,allUsers=allUsers,topKey=','.join(top3Key),categories=','.join(categoriesFind),check=checked_,neu=neu,neg=neg,pos=pos)

@app.route('/user', methods=['GET','POST'])
def userPage():
    errors = []
    arr = []
    result = ''
    tb_ = module.Category()
    categories = tb_.allCategories()
    for c in categories:
        arr.append(c['name'])
    if request.method == "POST":
        try:
            categoriesForUser = request.form.getlist('categories')
            categoriesForUser = ','.join(categoriesForUser)
            userName = request.form.get('userName')
            tb = module.Users()
            result = tb.create(userName,categoriesForUser,'')
        except:
            errors.append(
                "Unable add user name may duplicated."
            )
    return render_template('user.html',categories=arr, result=result, errors=errors)

@app.route('/feedback', methods=['GET'])
def feedback():
    userName = request.args.get('user')
    feedBack = request.args.get('feedback')
    tb = module.Users()
    tb.insertFeedBack(userName, feedBack)
    return "ok"

@app.route('/createCategory', methods=['GET'])
def createCategorys():
    name = request.args.get('name')
    keyword = request.args.get('keyword')
    tb = module.Category()
    result = tb.create(name,keyword)
    print(result)
    return result

@app.route('/updateCategory', methods=['GET'])
def updateCategory():
    name = request.args.get('name')
    keyword = request.args.get('keyword')
    tb = module.Category()
    result = tb.updateCategory(name,keyword)
    print(result)
    return result

@app.route('/deleteCategory', methods=['GET'])
def deleteCategory():
    name = request.args.get('name')
    tb = module.Category()
    result = tb.deleteCategory(name)
    print(result)
    return result

if __name__ == '__main__':
    app.run()
