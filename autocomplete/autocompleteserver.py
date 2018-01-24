import autocomplete
from flask import Flask, url_for, request



app = Flask(__name__)

autocomplete.load()


@app.route('/generateautocomplete')
def api_articles():
  
    response = []

    query = request.args.get('query').split(' ')
    
    subQuery = query[len(query)-1]
    
    result = autocomplete.predict(subQuery,'')
    
    if len(result)>=3:

        response = [result[0][0], result[1][0], result[2][0]]

    elif len(result)==2:

        response = [result[0][0], result[1][0]]

    elif len(result)==1:

        response = [result[0][0]]
    

    return str(response)



if __name__ == '__main__':
    app.run()
