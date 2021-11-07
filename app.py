from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
import os
import module

app = Flask(__name__)

categories = ['Technology', 'Food', 'Entertainment', 'Animation', 'Outdoor', 'BoardGame', 'Sport', 'Investment']

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
            selectedUser = tb.getByName(user)
            feedback_ = str(selectedUser.feedback)
            keyWords = feedback_    .split(',')
            currentCategories = str(selectedUser.categories)
            currentCategories = currentCategories.split(',')
            for c in currentCategories:
                k = tb_.getKeyWordByName(c)
                keyWords.append(k)
            print(keyWords)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    return render_template('index.html', errors=errors, result=result,allUsers=allUsers)

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
    tb = module.Users()
    tb.insertFeedBack(userName, 'new feedback')
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