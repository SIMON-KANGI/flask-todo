from flask import Flask, render_template, request, redirect ##import the libraries
from flask_sqlalchemy import SQLAlchemy ## make sure to install flask_sqlalchemy
from datetime import datetime
from flask_migrate import Migrate # get the migration files for updating the database when needed



app = Flask(__name__) # initialize the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #configure the databsabase using these commands
db = SQLAlchemy(app) # create a database instance
migrate = Migrate(app, db) # helps to update the database schema
class Todo(db.Model): # create a CLASS for todo
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)      # set the database structure /ORM
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Add status field
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): # representation
        return '<Todo %r>' % self.title
#app decorator for creating the filesystems
@app.route('/', methods=['POST','GET']) #CALL POST request and GET request METHODS
def home():
    if request.method == "POST":
        task = request.form['task']
        description = request.form['description']
        status = request.form['status']
        todo = Todo(title=task, description=description, status=status)
        try:
            db.session.add(todo)# add task to database
            db.session.commit() # COMMIT WORK
            return redirect('/')
        except Exception as e:
            print(e)
            return redirect('/')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('home.html', tasks=tasks)


@app.route('/delete/<int:id>') #delete a task
def delete(id):
    task_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(e)
        return redirect('/')
 # update a task   
@app.route('/update/<int:id>', methods=['POST', 'GET']) # call the post and get methods
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
    with app.app_context(): # create a context for the application
        db.create_all() #this will run the database when the app is run
    app.run(debug=True)
