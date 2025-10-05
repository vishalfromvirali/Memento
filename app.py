from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail,Message
from flask_apscheduler import APScheduler
import os
from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)
app.config['SCHEDULER_API_ENABLED'] = True 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587   
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='bb4106402@gmail.com'
app.config['MAIL_PASSWORD']='qjrhwiwnscjlsvbi'

mail=Mail(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo_list_new.db'

db=SQLAlchemy(app)
class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=False)
    mail=db.Column(db.String(50),nullable=False)
    time=db.Column(db.String(50),nullable=False)
    completed=db.Column(db.Boolean,default=False)

with app.app_context():
    db.create_all()



scheduler=APScheduler()
scheduler.init_app(app)
def scheduler_run():
    with app.app_context():
        
        current_time=datetime.now()
        formated_time=current_time.strftime("%Y-%m-%dT%H:%M")
        todo_list = db.session.execute(db.select(Todo).order_by(Todo.id)).scalars().all()
        for to in todo_list:
            t=to.time
            #print(t)
            if t==formated_time and to.completed==False:
                msg = Message(
                "Remainder", 
                sender='bb4106402@gmail.com', 
                recipients=[to.mail],
                body=(f"Hey there! 👋 Just sliding into your notifications with a gentle, but firm, nudge. It looks like the universe is still waiting for you to complete {to.title}. Don't let that amazing idea gather dust! You've already done the hard work of starting—now, let's smash that finish line. Quick, dive back in and get it done! You got this!")

            )
                print(f"message sended sucessfully{to.time}")
                to.completed=True
                db.session.commit()
                mail.send(msg)
                
scheduler.add_job(
    id='Scheduled Reminders', 
    func=scheduler_run, 
    trigger='interval', 
    minutes=1,
    start_date=datetime.now() 
)

scheduler.start() 

@app.route('/')
def get_all():
    todo_list = db.session.execute(db.select(Todo).order_by(Todo.id)).scalars().all()
    return render_template('index.html',todo_list=todo_list)


@app.route('/add',methods=['POST'])
def post():
    data=request.form.get('title')
    mail=request.form.get('mail')
    time=request.form.get('time_remainder')
    if(data=='delete all' and mail=='vishalfromvirali@gmail.com' ):
        num_db=db.session.query(Todo).delete()
        db.session.commit()
    else:
        new_data=Todo(title=data,mail=mail,time=time,completed=False)
        db.session.add(new_data)
        db.session.commit()
    
    return redirect(url_for('get_all'))
if __name__ =='__main__':
    app.run(debug=True)