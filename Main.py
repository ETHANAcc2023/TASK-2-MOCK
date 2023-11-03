from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/sign_up')
def sign_up_page():
    return render_template('sign_up_page.html')

if __name__ == '__main__':
    app.run(debug=True)