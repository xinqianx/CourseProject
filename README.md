# HyperLink Classification
Final Project CS410, UIUC

Group Name: *TTIS 5*
- Zhengkai Zhang (zz68) - Captain
- Yuan Chung Ho (ych11) 
- Wan Feng Cai (wfcai2) 
- Xinqian Xiang (xinqian6) 
- Zheng Ma (zhengma3

## Introduction
We receive a mass amount of information everyday, for example advertisements from email and 
push notifications from search engines, and it comes with a link to another page. We scan 
through titles and quickly make decisions whether we are interested or not. It is time 
consuming in searching through the interesting information. Therefore, we are encouraged 
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
People who want to know high levels of a given url without reading through all the text

## Installation requirement 


## Category Development
We obtain category in two ways: build category inventory in database and update category by users. First, we generate 
a category inventory in our database. We include 10 different categories, each contain top 30 keywords in terms of popularity. 
For example, swimming and table tennis are included in the sports category. Then, when users update their interest, 
category will also be added or updated.

## Algorithm Exploration
### Data Retrieval
Given the goal of the hyperlink classification, we first remove stop words and extract english words only. 

### Data Mining 
For the text data from the above step, we decide a threshold which depends on the length of the url text data size.
Similar to IDF, we set bigger threshold value for larger data set and smaller one for smaller data set.
We utilize a pre-trained model and nltk library to find the top frequent key phrases. 

## References
https://www.nltk.org/
