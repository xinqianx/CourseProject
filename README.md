# HyperLink Classification
Final Project CS410, UIUC

Group Name: *TTIS 5*
- Zhengkai Zhang (zz68) - Captain
- Yuan Chung Ho (ych11) 
- Wan Feng Cai (wfcai2) 
- Xinqian Xiang (xinqian6) 
- Zheng Ma (zhengma3)

## Introduction
We receive a mass amount of information everyday, for example advertisements from email and push notifications from search engines, and it comes with a link to another page. We scan through titles and quickly make decisions whether we are interested or not. It is time consuming in searching through the interesting information. Therefore, we are encouraged 
to seek a way to pick out useful information to make our life more efficient.

## Objective
We are presenting a tool called **HyperLink classification** that helps users to 
identify whether a link they receive from email or search engine (eg: google) meets 
their needs. 

The tool includes the following features:
- Develop a list of categories and corresponding keywords.
- The user profiles were built based on their selection of interesting categories.
- Scrape text from user-provided url. Remove stop words and rank text based on counts.
- Generate top key phrases about the text and perform sentiment analysis

We have 2 main code files
- `app.py`
- `module.py`

Packages required:
- mysql
- beautifulsoup
- Flask
- nltk

## Target users are
People who want to know high levels of a given url without reading through all the text.

## Installation requirement 
The `requirements.txt` file should list all Python libraries and they will be installed using:
`pip install -r requirements.txt`

## Steps to setup
1. git clone https://github.com/xinqianx/CourseProject.git
2. download postgreappp from https://postgresapp.com/
3. install the postgreapp and create a new server with port 5430
4. setup the password for server 5430's default user postgres with kaikai49 (code db link: "postgresql://postgres:kaikai49@localhost:5430")
5. source  source `venv/bin/activate`  (it include all package needed) if not have venv do `pip3 install requirements.txt` will install dependencies
6. `python3 import.py` (set up the default category)
7. `python3 app.py` (start the app)
8. http://127.0.0.1:5000/user router to create new user, http://127.0.0.1:5000 root router to use the app

## Front end
We developed two main front end: one is `/user` page which allows users to create new user profiles with their names and select categories for themselves. The root page of the UI is `app.user/admin` which is able to pick the user the created and input the url they want to classify. It will return the summary of the link, and user will able to select they like the link content or not.

## Back end
We defined APIs to update/delete/create/insert user's feedback. Also, we defined API to update/delete/create categories. With the router page, when user submit form of url. It will process the link with our scraping logic to get all the content. After get the content we will do the algorithm to get the classification result. Our logic will penilize the longer content and increase the threshold to pick an appeared word if it is in the longer document/web page. It will return the top keywords and categories for the web page, and we also compute the sentiment summary for the web page. It will decide if user has the same interested keywords with the web page and show the classifcation decision as yes or no. After User get the result, user can select yes interested with the link then it will add the top keyword to user's feedback list. Even the link don't has the user's interested categories if the user select yes. Next time user input similar web site with this website it could make decision become true since we add feedback from user as consideration. 

## Category Development
We obtain category in two ways: build category inventory in database and update category by users. First, we generate a category inventory in our database. We include 10 different categories, each contain top 30 keywords in terms of popularity. For example, swimming and table tennis are included in the sports category. Then, when users update their interest, 
category will also be added or updated.

## Algorithm Exploration
### Data Retrieval
Given the goal of the hyperlink classification, we first remove stop words and extract english words only. 

### Data Mining 
For the text data from the above step, we decided a changeable threshold which depends on the length of the url text data size. Similar to IDF, we set bigger threshold value for larger data set and smaller one for smaller data set.

In the end,we utilize a pre-trained model and nltk library to find the top frequent key phrases. The top keywords return to the user to help him or her make decision whether this url is interesting to him or her. The categories identified for the url can also assist users to identify whether they may like the link. For the sentiment analysis, we make judgement about the url which will also be a good reference for users.

## References
https://www.nltk.org/
