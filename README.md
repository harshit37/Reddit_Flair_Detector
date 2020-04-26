# Reddit_Flair_Detector
Deployed a machine learning model on Heroku which can predict the flair of a reddit post from subreddit r/India.
The application can be found live at [Reddit Flair Detector](https://rindia-flair-detector.herokuapp.com/).

## Codebase
The entire code has been developed using Python programming language, utilizing it's powerful text processing and machine learning modules. The application has been developed using Angular 7 for frontend and Flask for backend and hosted on Heroku web server.

## Dependencies

The following dependencies can be found in [requirements.txt](https://github.com/harshit37/Reddit_Flair_Detector/tree/master/backend_flask/requirements.txt):

    praw
    scikit-learn
    nltk
    Flask
    bs4
    pandas
    numpy
    seaborn
    matplotlib
    pickle
   
 ## Approach
 
 ### 1.Data Collection
 Code for which can be found [here](https://github.com/harshit37/Reddit_Flair_Detector/blob/master/Scrapping_Reddit_Data.ipynb).
 PRAW was used to scrape data from r/india . Data was collected in three stages to make a more robust model .
 
 These were the flairs = ["AskIndia", "Non-Political", "[R]eddiquette", "Scheduled", "Photography", "Science/Technology","Politics", "Business/Finance", "Policy/Economy","Sports", "Food", "AMA","Coronavirus"] corresponding to which data was scrapped . A limit of 500 posts was kept over each flair , PRAW returned different number of posts per flair at every stage of collection .
 Finally we had these many posts per flair
- AskIndia  -->  342
- Non-Political  -->  353
- [R]eddiquette  -->  0
- Scheduled  -->  350
- Photography  -->  343
- Science/Technology  -->  343
- Politics  -->  353
- Business/Finance  -->  344
- Policy/Economy  -->  344
- Sports  -->  310
- Food  -->  112
- AMA  -->  98
- Coronavirus  -->  249

It's pretty clear that our dataset is imbalanced due to less number of posts for flairs [AMA,Food,[R]eddiquette]

Besides, the problem is that models trained on unbalanced datasets often have poor results when they have to generalize (predict a class or classify unseen observations) and we also  cannot rely on accuracy as a good performance metric due to something called as Accuracy Paradox.

It is the case where your accuracy measures tell the story that you have excellent accuracy (such as 90%), but the accuracy is only reflecting the underlying class distribution ie you are not performing well on every class rather you are performing good on the class with maximum occurence in your dataset.

So model was chosen not only on the basis of accuracy but also on the basis of precision , recall ,F1 score and other metrics


    
 ### 2.Data Cleaning

    I've followed the following steps to clean the text of the posts.
    
    Convert words to Lowercase.
    Removed the stop-words.
    Removed the punctuation.
    I have used the same procedure to clean the post of new test cases on the web-app.
    Script for cleaning can be found in the EDA(Reddit_Data).ipynb

 ### 3.Exploratory Data Analysis
 
 Code for which can be found [here](https://github.com/harshit37/Reddit_Flair_Detector/blob/master/EDA(Reddit_data).ipynb)
 
 While doing the analysis, apart from discovering the imbalance in data these were other profound observations.
 
- Using Word Cloud 

This problem is difficult given the ambiguity between different flairs .
For example :- Frequently occuring words in coronavirus may suggest that the flair is business/finance or vice-versa
The flair coronavirus has actually a great overlap with many other flairs (in terms of frequently occuring words)like politics,sports,business/finance,policy/economy.
So the machine learning model should focus on relations between words and in what context they are being used .

- Plot (No. of comments VS No. of posts)

Most of them have close to 20-25 comments and after looking the comments by going to reddit India , it is not a good idea to keep a threshold greater than 20 as after that comments generally do not provide useful information.

- No. of words in body VS No. of posts / No. of words in title VS No. of posts

To decide which input should be chosen as the features (whether that feature is reliable or not)


### 4.Flair Detection

First standalone features were tried like comments, title, body, url .etc. However the classification report was not upto the mark. The average accuracy remained around 50-55%. After that, many features were combined on the basis of their standlone accuracies , title and comments were the best performing features as per their standalone classification report . The combination of features that gave the best accuracy (55-68%) was that of title,comments,url and body, with Logistic Regression giving the best accuracy(68%). 

Basically five ML algorithms were used:

    Naive Bayes
    Linear Suport Vector Machine
    Logistic Regression
    Random Forest
    Multi Layer Perceptron

#### Results

Combined features turned out to be the best choice as compared to standalone features . 
Now , among the above 5 ML algorthims which were trained on combined features Logistic Regression performed the best followed by 
Random Forest and then Linear Support Vector Machine(as per the classification report)

##### Where does the model lack ?

Coronavirus flair intersects with many other flairs like politics,business/finance,non-political and poliy/economy so model faces difficulty in identifying posts tagged as coronavirus . 
For example :- If there is a post related to economic slowdown , now this is because of coronavirus but technically it should be given the flair Business/Economics .
So, I think this is the ambiguity which humans will also face given this task .

The same issue is faced for the flair Non-Political , sometimes the comments drive the predicted flair away from the correct flair . 
For example :- If there is a post related to attack on Arnab Goswami should it be considered under politics or Non-political.

Also,since training samples were less for AMA,Food,[R]eddiquette thus model faces difficulty in classifying them.

##### What is the model good at?

Despite repeated occuring of name of other flairs like food in a post with actual flair let say Photography,Business/Finance etc it doesn't divert from the actual flair .
                
### 5.Building A web Application

For frontend, Angular 7 is used. To setup the local dev environment refer to [README.md](https://github.com/harshit37/Reddit_Flair_Detector/blob/master/frontend_angular/README.md)
Run "npm install" to install all the modules listed as dependencies in package.json
After installing the dependencies walkthrough the code given [here](https://github.com/harshit37/Reddit_Flair_Detector/tree/master/frontend_angular)

For Backend, Flask is used which is a micro web framework. For installing all the backend dependencies refer [here](https://github.com/harshit37/Reddit_Flair_Detector/tree/master/backend_flask/requirements.txt)
After installing the dependencies walkthrough the code given [here](https://github.com/harshit37/Reddit_Flair_Detector/tree/master/backend_flask)

@cross_origin() decorator is used to allow Cross-origin resource sharing (CORS) which is used in [main.py](https://github.com/harshit37/Reddit_Flair_Detector/blob/master/backend_flask/app/main.py)

### 6.Deploying on Heroku
1) Go to Heroku.com and signup.
2) Create an app by giving a unique app name.
3) Refer deployement steps given [here](https://dashboard.heroku.com/apps/rindia-flair-detector/deploy/heroku-git)

 ## Build on Google Colab

Google Colab lets us build the project without installing it locally. Installation of some libraries may take some time depending on your internet connection.
All the .ipynb files can be found [here](https://github.com/harshit37/Reddit_Flair_Detector).
To get started, open the notebooks in playground mode and run the cells(You must be logged in with your google account and provide additional authorization). 

## Steps For Automated Testing
1) You need a file containing valid URL's from reddit india in each line. Refer to sample [file.txt](https://github.com/harshit37/Reddit_Flair_Detector/blob/master/backend_flask/file.txt).
2) Install python and run 2 lines of code as mentioned below.
Automated Testing link is "https://flair-detection-backend.herokuapp.com/automated_testing" where you can post your request.

import requests

files = {'upload_file': open('path to file.txt','rb')}

r = requests.post("https://flair-detection-backend.herokuapp.com/automated_testing", files=files)

print(r.text)

Response from the above API is (r) which will be in json format where keys will be the link to the post and values will be the predicted flair. r.text is used to display the json response.

## References
##### For Data Collection
1) http://machineloveus.com/mining-reddit-data-or-links-to-33-python-cheat-sheets/
2) http://www.storybench.org/how-to-scrape-reddit-with-python/

##### For deployment on heroku
1)https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0

##### To enable cors in flask
2)https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask

