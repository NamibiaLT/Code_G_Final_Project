# Code_G_Final_Project
This was developed with an Anaconda installation of Python 3.7

Installation Steps:

1. OPTIONAL create and activate a new virtual environment
    
    With Anaconda:
    
        conda create -n ve python=3.7
        conda activate ve
        
2. Install requirements. As some of the dependencies are not available in the conda repo, we use pip to install all libraries.

```
pip install -r requirements.txt
```

3. Run the FLASK application
        
    Change directory to `Code_G_Final_Project`. For debugging, you can add `export FLASK_DEBUG=1`

```
Code_G_Final_Project$ export FLASK_APP=server.py
Code_G_Final_Project$ flask run
```


## Scripts
#### To generate cleaned employee_reviews.csv for NLP:
```
Code_G_Final_Project/reviews_app/model$ python parse_kaggle.py
```
This generates a file called `employee_reviews.cleaned.csv`

#### To generate word cloud images from employee_reviews
#####Note: you will need to use `pythonw` instead of `python` for Anaconda installations of python. 
To install `pythonw` in Anaconda environment, run `conda install python.app`

```
Code_G_Final_Project/reviews_app/model$ pythonw review_wordcloud.py
```
This generates a 1000 x 1000 word cloud based on the summary, pros, and cons reviews for each company in the dataset.
Word cloud image files are downloaded to reviews_app/model/images


## Testing

We have set up some unit tests with the `pytest` library

To run the tests you will have to install the test requirements:

```bash
pip install -r test_requirements.txt
```

Then to run these tests, go to the top level directory of the project then issue the following command:

```bash
python -m pytest .
```

### Writing a test

Pytest will discover test cases by first looking for files in the `tests/` directory then looking within this directory for test files that start with the prefix `test_`.

All functions that start with `test` will then be run by the Pytest runner. (for example `test_homepage` function in `tests/test_homepage.py` will be automatically run.`
