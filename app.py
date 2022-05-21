from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///project.sqlite3'
app.config['SECRET_KEY']='project'
app.config['UPLOAD_FOLDER']='./static/uploads/'

db=SQLAlchemy(app)

class accounts(db.Model):
    id=db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    a_id=db.Column(db.String(30))
    a_password=db.Column(db.String(30))
    a_nickname=db.Column(db.String(30))
    
    def __init__(self, id, password, nickname):
        self.a_id=id
        self.a_password=password
        self.a_nickname=nickname
        
class posts(db.Model):
    id=db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    p_title=db.Column(db.String(30))
    p_keyword=db.Column(db.String(30))
    p_price=db.Column(db.String(30))
    p_seller=db.Column(db.String(30))
    p_description=db.Column(db.String(300))
    p_image1=db.Column(db.String(30))
    p_image2=db.Column(db.String(30))
    p_image3=db.Column(db.String(30))
    p_soldOut=db.Column(db.Boolean, default=False)
    
    def __init__(self, title, price, keyword, description, seller, image1, image2, image3):
        self.p_title=title
        self.p_keyword=keyword
        self.p_price=price
        self.p_seller=seller
        self.p_description=description
        self.p_image1=image1
        self.p_image2=image2
        self.p_image3=image3

@app.route('/')
def home():
    global signUpId
    global signUpPassword
    global signUpNickname
    global isIdDuplicate
    global isNicknameDuplicate
    
    global signInId
    global signInPassword
    
    global registerTitle
    global registerPrice
    global registerDescription
    global registerimage1
    global registerimage2
    global registerimage3
    # 홈에 오면 회원가입에 사용했던 값들을 초기화
    signUpId=''
    signUpPassword=''
    signUpNickname=''
    isIdDuplicate=True
    isNicknameDuplicate=True
    
    signInId=''
    signInPassword=''
    
    registerTitle=''
    registerPrice=''
    registerDescription=''
    registerimage1=''
    registerimage2=''
    registerimage3='' 
    return render_template('home.html')

# 회원가입 페이지에서 입력 값을 기억하는 변수들
signUpId=''
signUpPassword=''
signUpNickname=''
isIdDuplicate=True
isNicknameDuplicate=True

@app.route('/signUp/', methods=['GET', 'POST'])
def signUp():
    global signUpId
    global signUpPassword
    global signUpNickname
    global isIdDuplicate
    global isNicknameDuplicate
    
    if request.method=='POST':
        # 폼의 일부분이 비어있으면
        if not request.form['a_id'] or not request.form['a_password'] or not request.form['a_nickname']:
            flash('Please enter all the fields', 'error')
            signUpId=request.form['a_id']
            signUpPassword=request.form['a_password']
            signUpNickname=request.form['a_nickname']
        # 아이디 중복 확인을 하지 않았으면
        elif isIdDuplicate==True:
            flash('Please check duplication of id', 'error')
            signUpId=request.form['a_id']
            signUpPassword=request.form['a_password']
            signUpNickname=request.form['a_nickname']
        # 닉네임 중복 확인을 하지 않았으면
        elif isNicknameDuplicate==True:
            flash('Please check duplication of nickname', 'error')
            signUpId=request.form['a_id']
            signUpPassword=request.form['a_password']
            signUpNickname=request.form['a_nickname']
        # 아이디 또는 닉네임의 중복 확인을 했으나 중복 확인 후 값을 바꿨다면
        elif request.form['a_id']!=signUpId or request.form['a_nickname']!=signUpNickname:
            flash('your inserted id or nickname changed, please check both duplication again', 'error')
            signUpId=request.form['a_id']
            signUpPassword=request.form['a_password']
            signUpNickname=request.form['a_nickname']
            isIdDuplicate==True
            isNicknameDuplicate==True
        # 문제가 없으면 회원 가입을 진행
        else:
            account=accounts(request.form['a_id'], request.form['a_password'], request.form['a_nickname'])
            db.session.add(account)
            db.session.commit()
            flash('Record was successfully added')
            signUpId=''
            signUpPassword=''
            signUpNickname=''
            isIdDuplicate=True
            isNicknameDuplicate=True
            return redirect(url_for('home'))
    # GET이었거나 POST에서 문제가 생겼으면 현재까지 입력 값을 이용해 다시 랜더링
    return render_template('signUp.html', id=signUpId, password=signUpPassword,nickname=signUpNickname)


@app.route('/idDuplicateCheck/', methods=['GET', 'POST'])
# 아이디 중복 확인
def idDuplicateCheck():
    global signUpId
    global signUpPassword
    global isIdDuplicate
    # 다시 랜더링 하기 위해 현재 비밀번호를 기억해둔다
    signUpPassword=request.form['a_password']
    
    if not request.form['a_id']:
        flash('Please enter new id')
        return redirect(url_for('signUp'))
    
    if request.method=='POST':
        # 입력 아이디와 일치하는 아이디가 있는지 찾는다
        id=accounts.query.filter_by(a_id=request.form['a_id']).first()
        # 일치하는 것이 존재하면 새로운 아이디를 입력하게 한다
        if(id):
            flash('Id is already exists. Please enter new Id')
            
            signUpId =''
            isIdDuplicate=True
            return redirect(url_for('signUp'))
        # 일치하는 것이 존재하지 않으면 기존 입력 값을 이용해 랜더링하고 회원가입을 이어서 진행하게 한다
        else:
            flash('Id is not exists. You can use it')
            signUpId=request.form['a_id']
            isIdDuplicate=False
            return redirect(url_for('signUp'))
        
@app.route('/NicknameDuplicateCheck/', methods=['GET', 'POST'])
# 닉네임 중복 확인
def NicknameDuplicateCheck():
    global signUpNickname
    global signUpPassword
    global isNicknameDuplicate
    # 다시 랜더링 하기 위해 현재 비밀번호를 기억해둔다
    signUpPassword=request.form['a_password']
    
    if not request.form['a_nickname']:
        flash('Please enter new nickname')
        return redirect(url_for('signUp'))
    
    if request.method=='POST':
        # 입력 닉네임과 일치하는 닉네임이 있는지 찾는다
        nickname=accounts.query.filter_by(a_nickname=request.form['a_nickname']).first()
        # 일치하는 것이 존재하면 새로운 닉네임을 입력하게 한다
        if(nickname):
            flash('Nickname is already exists. Please enter new Nickname')
            
            signUpNickname =''
            isNicknameDuplicate=True
            return redirect(url_for('signUp'))
        # 일치하는 것이 존재하지 않으면 기존 입력 값을 이용해 랜더링하고 회원가입을 이어서 진행하게 한다
        else:
            flash('Nickname is not exists. You can use it')
            signUpNickname=request.form['a_nickname']
            isNicknameDuplicate=False
            return redirect(url_for('signUp'))
        
        
signInId=''
signInPassword=''
@app.route('/signIn/', methods=['GET', 'POST'])
def signIn():
    global signInId
    global signInPassword
    
    if request.method=='POST':
        if not request.form['a_id'] or not request.form['a_password']:
            flash('Please enter all the fields', 'error')
            signInId=request.form['a_id']
            signInPassword=request.form['a_password']
            return redirect(url_for('signIn'))
        
        account=accounts.query.filter_by(a_id=request.form['a_id']).first()
        if not account:
            flash('id is not exists')
            signInId=''
            signInPassword=''
            return redirect(url_for('signIn'))
        elif account.a_password!=request.form['a_password']:
            signInId=request.form['a_id']
            signInPassword=''
            flash('password is wrong')
            return redirect(url_for('signIn'))
        else:
            signInId=''
            signInPassword=''
            flash('Sign in success')
            session['nickname']=account.a_nickname
            return redirect(url_for('home'))
    return render_template('signIn.html', id=signInId,password=signInPassword)

@app.route('/signOut/', methods=['GET', 'POST'])
def signOut():
    session.pop('nickname',None)
    flash('Sign Out success')
    return redirect(url_for('home'))
       
registerTitle=''
registerPrice=''
registerDescription=''
registerimage1=''
registerimage2=''
registerimage3='' 
@app.route('/register/', methods=['GET','POST'])
def register():
    global registerTitle
    global registerPrice
    global registerDescription
    global registerimage1
    global registerimage2
    global registerimage3
    
    if 'nickname' not in session:
        flash('you must sign in to register a product')
        return redirect(url_for('signIn'))
    
    if request.method=='POST':        
        if not request.form['p_title'] or not request.form['p_price'] or request.form['p_keyword']=='키워드 *':
            flash('제목, 가격, 키워드는 필수로 작성해야합니다.')
            registerTitle=request.form['p_title']
            registerPrice=request.form['p_price']
            registerDescription=request.form['p_description']
        else:
            if request.files['p_image1']:
                f1=request.files['p_image1']
                registerimage1=f1.filename
                f1.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f1.filename)))
            if request.files['p_image2']:
                f2=request.files['p_image2']
                registerimage2=f2.filename
                f2.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f2.filename)))
            if request.files['p_image3']:
                f3=request.files['p_image3']
                registerimage3=f3.filename
                f3.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f3.filename)))
            
            post=posts(request.form['p_title'], request.form['p_price'], request.form['p_keyword'], request.form['p_description'], session['nickname'],
                       registerimage1,registerimage2,registerimage3)
            db.session.add(post)
            db.session.commit()
            registerTitle=''
            registerPrice=''
            registerDescription=''
            registerimage1=''
            registerimage2=''
            registerimage3='' 
            flash('Record was successfully added')
            return redirect(url_for('home'))
            
    return render_template('register.html', title=registerTitle, price=registerPrice, description=registerDescription)

        
@app.route('/search/<keyword>', methods=['GET','POST'])
def search(keyword):
    if keyword=='all':
        list=posts.query.all()
        print(len(list))
        return render_template('search.html', list=list, keyword=keyword)
    elif keyword=='keyword':
        temp=request.form['searchBar']
        return redirect(url_for('search',keyword=temp))
    else:
        if keyword=='default':
            flash('키워드를 선택한 후, 검색해주세요')
            return redirect(url_for('search',keyword='all'))
        list=posts.query.filter_by(p_keyword=keyword)
        return render_template('search.html', list=list, keyword=keyword)
           
    
@app.route('/detail/<id>', methods=['GET','POST'])
def detail(id):
    post=posts.query.filter_by(id=id).first()
    return render_template('detail.html', post=post) 

@app.route('/image/<name>', methods=['GET','POST'])
def image(name):
    return render_template('image.html', image=name)     

@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    post=posts.query.filter_by(id=id).first()
    return render_template('edit.html', title=post.p_title, price=post.p_price, description=post.p_description,id=id) 

updateTitle=''
updatePrice=''
updateDescription=''
updateimage1=''
updateimage2=''
updateimage3='' 
@app.route('/update/<id>', methods=['GET','POST'])
def update(id):
    global updateTitle
    global updatePrice
    global updateDescription
    global updateimage1
    global updateimage2
    global updateimage3
    
    if not request.form['p_title'] or not request.form['p_price'] or request.form['p_keyword']=='키워드 *':
            flash('제목, 가격, 키워드는 필수로 작성해야합니다.')
            updateTitle=request.form['p_title']
            updatePrice=request.form['p_price']
            updateDescription=request.form['p_description']
            return redirect(url_for('edit',id=id))
    else:
        if request.files['p_image1']:
            f1=request.files['p_image1']
            updateimage1=f1.filename
            f1.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f1.filename)))
        if request.files['p_image2']:
            f2=request.files['p_image2']
            updateimage2=f2.filename
            f2.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f2.filename)))
        if request.files['p_image3']:
            f3=request.files['p_image3']
            updateimage3=f3.filename
            f3.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f3.filename)))
        
        post=posts.query.filter_by(id=id).first()
        post.id=id
        post.p_title= request.form['p_title']
        post.p_keyword= request.form['p_keyword']
        post.p_price= request.form['p_price']
        post.p_seller=session['nickname']
        post.p_description=request.form['p_description']
        post.p_image1=updateimage1
        post.p_image2=updateimage2
        post.p_image3=updateimage3
        post.p_soldOut=False
        db.session.commit()
        updateTitle=''
        updatePrice=''
        updateDescription=''
        updateimage1=''
        updateimage2=''
        updateimage3='' 
        flash('Record was successfully added')
        return redirect(url_for('detail',id=id))

@app.route('/follow/')
def follow():
    return render_template('follow.html')

@app.route('/manage/')
def manage():
    return render_template('follow.html')

@app.route('/profile/')
def profile():
    return render_template('follow.html')
    

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)

    