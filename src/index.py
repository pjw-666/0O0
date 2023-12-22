from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/s_t_学号'
# 关闭动态追踪修改的警告信息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 展示sql语句
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='secret123'
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
class student(db.Model):
    __tablename__ ='student'
    Sno= db.Column(db.String(9), primary_key=True)
    Sname = db.Column(db.String(20))
    Ssex = db.Column(db.String(2))
    Sage = db.Column(db.Integer)
    Sdept = db.Column(db.String(20))
    Scholarship= db.Column(db.String(2))
    def __init__(self,Sno,Sname,Ssex,Sage,Sdept,Scholarship):
        self.Sno=Sno
        self.Sname=Sname
        self.Ssex=Ssex
        self.Sage=Sage
        self.Sdept=Sdept
        self.Scholarship=Scholarship


class course(db.Model):
    __tablename__ ='course'
    Cno=db.Column(db.String(4), primary_key=True)
    Cname=db.Column(db.String(40))
    Cpno=db.Column(db.String(4))
    Ccredit=db.Column(db.Integer)
    def __init__(self,Cno,Cname,Cpon,Ccredit):
        self.Cno=Cno
        self.Cname=Cname
        self.Cpon=Cpon
        self.Ccredit=Ccredit

class sc(db.Model):
    __tablename__='sc'
    Sno=db.Column(db.String(9))
    Cno=db.Column(db.String(4))
    Grade=db.Column(db.Integer,primary_key=True)
    def __init__(self,Sno,Cno,Grade):
        self.Sno=Sno
        self.Cno=Cno
        self.Grade=Grade

@app.route('/')
def show_student_info():
    return render_template('index.html', students=student.query.all())

@app.route('/add' ,methods = ['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['Sno'] or not request.form['Sname'] or not request.form['Ssex'] or not request.form['Sage']or not request.form['Sdept']or not request.form['Scholarship']:
            flash('请填入完整信息', 'error')
        else:
            students =student(request.form['Sno'], request.form['Sname'],request.form['Ssex'], request.form['Sage'],request.form['Sdept'],request.form['Scholarship'])
            db.session.add(students)
            db.session.commit()
            flash('添加成功')
            return redirect(url_for('show_student_info'))
    return render_template('add.html')

@app.route('/update/<id>',methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        print(url_for('new'))
        student.query.filter_by(Sno=id).update({'Sno': request.form['Sno'] , 'Sname' : request.form['Sname'],'Ssex':request.form['Ssex'],'Sage':request.form['Sage'],'Sdept':request.form['Sdept'],'Scholarship':request.form['Scholarship']})
        db.session.commit()
        return redirect(url_for('show_student_info'))
    else:
        return render_template('update.html', students=student.query.filter_by(Sno=id).all())

@app.route('/delete/<id>')
def delete(id):
    student.query.filter_by(Sno=id).delete()
    flash('删除成功')
    return redirect(url_for('show_student_info'))

@app.route('/course_info')
def course_info():
    return render_template('course_index.html', courses=course.query.all())

@app.route('/course/add' ,methods = ['GET', 'POST'])
def course_add():
    if request.method == 'POST':
        if not request.form['Cno'] or not request.form['Cname'] or not request.form['Cpno'] or not request.form['Ccredit']:
            flash('请填入完整信息', 'error')
        else:
            courses =course(request.form['Cno'], request.form['Cname'],request.form['Cpno'], request.form['Ccredit'])
            db.session.add(courses)
            db.session.commit()
            flash('添加成功')
            return redirect(url_for('course_info'))
    return render_template('course_add.html')

@app.route('/course/update/<id>',methods=['GET', 'POST'])
def course_update(id):
    if request.method == 'POST':
        course.query.filter_by(Cno=id).update({'Cno': request.form['Cno'] , 'Cname' : request.form['Cname'],'Cpno':request.form['Cpno'],'Ccredit':request.form['Ccredit']})
        db.session.commit()
        return redirect(url_for('course_info'))
    else:
        return render_template('course_update.html', courses=course.query.filter_by(Cno=id).all())

@app.route('/course/delete/<id>')
def course_delete(id):
    course.query.filter_by(Cno=id).delete()
    flash('删除成功')
    return redirect(url_for('course_info'))

@app.route('/sc_info')
def sc_info():
    return render_template('sc_index.html', scs=sc.query.all())

@app.route('/sc/add' ,methods = ['GET', 'POST'])
def sc_add():
    if request.method == 'POST':
        if not request.form['Sno'] or not request.form['Cno'] or not request.form['Grade']:
            flash('请填入完整信息', 'error')
        else:
            scs =sc(request.form['Sno'], request.form['Cno'],request.form['Grade'])
            db.session.add(scs)
            db.session.commit()
            flash('添加成功')
            return redirect(url_for('sc_info'))
    return render_template('sc_add.html')

@app.route('/sc/update/<cid>/<sid>',methods=['GET', 'POST'])
def sc_update(cid,sid):
    if request.method == 'POST':
        sc.query.filter_by(Cno=cid,Sno=sid).update({'Sno': request.form['Sno'] , 'Cno' : request.form['Cno'],'Grade':request.form['Grade']})
        db.session.commit()
        return redirect(url_for('sc_info'))
    else:
        return render_template('sc_update.html', scs=sc.query.filter_by(Cno=cid,Sno=sid).all())


@app.route('/sc/delete/<cid>/<sid>')
def sc_delete(cid,sid):
    sc.query.filter_by(Cno=cid,Sno=sid).delete()
    flash('删除成功')
    return redirect(url_for('sc_info'))

@app.route('/dept/data')
def sdept_data():
    datas = db.session.execute(text('select sdept,max(Grade) as max,min(Grade) as min,avg(Grade) as avg from student,sc where student.Sno=sc.Sno group by Sdept'))
    bujiges=db.session.execute(text('select sdept,count(grade) as bujig from student,sc where student.Sno=sc.Sno and grade<60 group by Sdept'))
    goods=db.session.execute(text('select sdept,count(grade) as youxiu from student,sc where student.Sno=sc.Sno and grade>=90 group by Sdept'))
    nums=db.session.execute(text('select sdept,count(grade) as gong from student,sc where student.Sno=sc.Sno group by Sdept'))
    zong=db.session.execute(text('select b.sdept,max(Grade) as max,min(Grade) as min,avg(Grade) as avg,bujig,youxiu,gong from student,sc,(select sdept,count(grade) as bujig from student,sc where student.Sno=sc.Sno and grade<60 group by Sdept)as b,(select sdept,count(grade) as youxiu from student,sc where student.Sno=sc.Sno and grade>=90 group by Sdept)as c ,(select sdept,count(grade) as gong from student,sc where student.Sno=sc.Sno group by Sdept)as d where student.Sno=sc.Sno and student.sdept=b.sdept and b.sdept=c.sdept and c.sdept=d.sdept group by Sdept'))
    return render_template('dept_data.html',zongs=zong)

@app.route('/dept/rank')
def sdept_rank():
    rank=db.session.execute(text('select student.Sno,Sname,Cname,Grade from student,course,sc where student.Sno=sc.sno and sc.cno=course.cno order by grade'))
    return render_template('rank.html', ranks=rank)

@app.route('/search',methods=['get','post'])
def search():
    if request.method=='POST':
        id=request.form['Sno']
        sql='select student.Sno,Sname,Sage,Ssex,Sdept,Cname from student,sc,course where student.Sno=sc.Sno and sc.Cno=course.Cno and student.Sno=%s'%(id)
        results=db.session.execute(text(sql))
        return render_template('search_result.html',results=results)
    else:
        return redirect('/')
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8080)
