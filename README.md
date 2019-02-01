# Code_G_Final_Project

## Running FLASK application
Change directory to `Code_G_Final_Project`. For debugging, can add `export FLASK_DEBUG=1`

```
Code_G_Final_Project$ export FLASK_APP=server.py
Code_G_Final_Project$ flask run
```

## To generate cleaned employee_reviews.csv for NLP:
```
Code_G_Final_Project/reviews_app/model$ python parse_kaggle.py
```
Generates file called `employee_reviews.cleaned.csv`

## To install required packages:
`pip install -r`
