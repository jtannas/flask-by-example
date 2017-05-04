"""
Simple Flask application.
"""

### IMPORTS ###################################################################
import operator
import os
import requests
from collections import Counter
from flask import Flask, render_template, request
from models import db, Result

from text_processing import get_request_natural_language

### APPLICATION ###############################################################
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


### VIEWS #####################################################################
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index Page. Serves and processes a form that gets a URL from the
    user.
    """
    errors = []
    html_results = {}
    if request.method == 'POST':
        try:
            url = request.form['url']
            r = requests.get(url)
        except:
            errors.append(
                'Unable to get URL. Please make sure it is valid and try again.'
            )
            return render_template('index.html', errors=errors)

        if r is not None:

            ### Get the Natural Language ###
            word_lists = get_request_natural_language(r)

            ### Perform the word counts ###
            raw_words_count = Counter(word_lists['raw'])
            no_stop_words_count = Counter(word_lists['no_stops'])

            ### Prepare the results ###
            html_results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True, )[:10]

            db_result = Result(
                url=url,
                result_all=raw_words_count,
                result_no_stop_words=no_stop_words_count)

            ### Save the results ###
            try:
                db.session.add(db_result)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")

    return render_template('index.html', errors=errors, results=html_results)


### RUN MAIN ##################################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
