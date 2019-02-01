from flask import render_template, Blueprint
from flask import request

backend_blueprint = Blueprint("backend", __name__)

@backend_blueprint.route("/")
def index():
    return render_template('index.html')


# SHOW ACTION TEMPLATE- where we send users after they hit submit
@backend_blueprint.route("/company_results")
def show():
    company_id = request.args.get("SAMPLE", type=str) # Pass in string as the argument name in get
    data = get_company_data(company_id)
    return render_template('company_results.html', context=data)

