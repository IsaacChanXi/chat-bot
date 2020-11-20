import os

from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from chat import predict_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret here'

class MyForm(FlaskForm):
    message = TextAreaField("What would like to speak about?")
    submit = SubmitField("Chat!")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        input_text = form.message.data 
        reply = predict_response(input_text)
        session['input'] = "User: {}".format(input_text)
        session['reply'] = "Movie Bot: {}".format(reply)
        return redirect(url_for('chat_more'))
    return render_template('my_home.html', form=form)

@app.route('/completed')
def chat_more():
    input_text = session['input']
    reply = session['reply']
    return render_template('completed.html', input_text=input_text, reply=reply)

@app.route('/delete')
def delete_history():
    if os.path.exists("history.txt"):
        os.remove("history.txt")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)