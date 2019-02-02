from flask import render_template, Blueprint
from flask import request
import pandas as pd

backend_blueprint = Blueprint("backend", __name__)
NLP_FILE = pd.read_csv("nlp.csv")



@backend_blueprint.route("/")
def index():
    return render_template('index.html')


# SHOW ACTION TEMPLATE- where we send users after they hit submit
@backend_blueprint.route("/company_results")
def show():
    company_id = request.args.get("SAMPLE", type=str) # Pass in string as the argument name in get
    data = get_company_data(company_id)
    # ['google', 'amazon', 'facebook', 'netflix', 'apple', 'microsoft']
    return render_template('company_results.html', context=data)


def get_nlp(company):
    # company pro pro pro con con con
    company = company.lower()
    df = NLP_FILE
    company_df = df[df['company'] == company]
    pro_list = [company_df['p1'].to_string(index=False).strip(), company_df['p2'].to_string(index=False).strip(),
                company_df['p3'].to_string(index=False).strip()]
    con_list = [company_df['c1'].to_string(index=False).strip(), company_df['c2'].to_string(index=False).strip(),
                company_df['c3'].to_string(index=False).strip()]
    return (pro_list, con_list)


@backend_blueprint.route("/wordcloud")
def company_wordcloud():
    company = request.args.get("company", type=str).lower()
    if company in ['amazon', 'google']:
        pro_list, con_list = get_nlp(company)
        return render_template('company_wordcloud.html', company=company, pro_list=pro_list, con_list=con_list)
    else:
        return render_template('company_wordcloud.html', company=company)


