from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Manvi%409072@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = "list"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.String(200), default='No')

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if(request.method=='POST'):
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
        
    else:
        tasks=Todo.query.order_by(Todo.id).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_del = Todo.query.get_or_404(id)
    try :
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return "Couldn't delete your task"

@app.route('/update/<int:id>', methods=['GET','POST']) 
def update(id):
    task = Todo.query.get_or_404(id)
    if(request.method=='POST'):
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Unable to update your content"
    else :
        return render_template('update.html',task=task)

if __name__=="__main__":
    app.run(debug=True)
