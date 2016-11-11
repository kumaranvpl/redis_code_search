import sys
import time

from code_search import CodeSearch

from flask import Flask, render_template
from flask import jsonify, request

from StringIO import StringIO


app = Flask(__name__)

app.secret_key = "some_random_really_secret_and_confidential_key"


def create_return_msg(status, msg, additional_msg=None):
    status_dict = {
        "status": status,
        "message": msg
    }
    if additional_msg is not None:
        status_dict.update(additional_msg)
    return status_dict


@app.errorhandler(404)
def page_not_found(e):
    return "Oops... This page doesn't exists :p"


@app.route('/')
def render_index():
    return render_template('search.html')


@app.route('/search', methods=["POST", "GET"])
def search_keyword():
    search_word = str(request.values.get('search_word'))
    word_type = str(request.values.get('word_type'))
    if not search_word:
        return jsonify(create_return_msg("error", "Search failed", {"exception": "Search Word can't be empty"}))
    #print search_word, type(search_word)
    try:
        redis_search = CodeSearch()

        old_stdout = sys.stdout
        result = StringIO()
        sys.stdout = result

        start_time = time.time()
        redis_search.redis_search(search_word, word_type)
        end_time = time.time()
        sys.stdout = old_stdout
        result_string = result.getvalue()
        return jsonify(create_return_msg("ok", "Search completed", {"result": result_string, "time": "%s seconds"%(end_time-start_time)}))
    except Exception as e:
        return jsonify(create_return_msg("error", "Search failed", {"exception": str(e)}))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
