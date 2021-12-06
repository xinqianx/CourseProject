# HyperLink Classification
Final Project CS410, UIUC

Group Name: *TTIS 5*
- Zhengkai Zhang (zz68) - Captain
- Yuan Chung Ho (ych11) 
- Wan Feng Cai (wfcai2) 
- Xinqian Xiang (xinqian6) 
- Zheng Ma (zhengma3



## Introduction
We are presenting a tool called **HyperLink classification** 

The tool includes the following features.
- Develop a list of categories and corresponding key words
- Scrape text from user-provided url
- Generate top key phrases about the text and sentiment

## Target users are
People who want to know high levels of a given url without reading through all the text


## Installation requirement 


## Category Development
We obtain category in two ways: build category inventory in database and update category by users. First, we generate a category inventory in our database. We include 10 different categories, each contain top 30 keywords in terms of popularity. For example, swimming and table tennis are included in the sports category. Then, when users update their interest, category will also be added or updated.

## Algorithm Exploration
Given the goal of the hyperlink classification, we first remove stop words and extract english words only. We also utilize a pre-trained model and nltk library to get the top frequent key phrases.


## References
https://www.nltk.org/
