import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
books = pd.read_csv("../data/books.csv")

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    first_title = books.iloc[0].title
    return render_template('index.html', titles=[first_title])
  

@app.route('/bestof')
def bestof():

    # This will render the bestof.html Please see that file. 
    return render_template('bestof.html')

def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
