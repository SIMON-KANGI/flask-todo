from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Add status field
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Todo %r>' % self.title

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == "POST":
        task = request.form['task']
        description = request.form['description']
        status = request.form['status']
        todo = Todo(title=task, description=description, status=status)
        try:
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return redirect('/')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)
        return redirect('/')
    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == "POST":
        task.title=request.form['task']
        task.description=request.form['description']
        task.status=request.form['status']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return redirect('/')
    else:
        return render_template('update.html', task=task)    
    
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
