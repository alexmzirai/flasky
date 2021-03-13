from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# note that 4 forward slashes is an absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)   # initialize db by passing in the app


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user should not leave task content empty
    content = db.Column(db.String, nullable=False)
    #completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# erplicate the code as described here


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)  # add the new task to the db
            db.session.commit()
            # afer commiting, send user back to the main page
            return redirect('/')

        except:
            return "there was an issue updating your new task!"

    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "I am unable to comply with your demand !"


@app.route('/update/<int:id>')
def update(id):
    pass # for now 


if __name__ == "__main__":
    app.run(debug=True)

