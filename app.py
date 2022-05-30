from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///project.sqlite3'
app.config['SECRET_KEY']='project'
app.config['UPLOAD_FOLDER']='./static/uploads/' # 상품 이미지 파일이 저장되는 경로

db=SQLAlchemy(app)

# 계정 데이터베이스
class accounts(db.Model):
    id=db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    a_id=db.Column(db.String(30), nullable=False, unique=True)
    a_password=db.Column(db.String(30))
    a_nickname=db.Column(db.String(30), nullable=False, unique=True)
    
    def __init__(self, id, password, nickname):
        self.a_id=id
        self.a_password=password
        self.a_nickname=nickname

# 판매 글 데이터베이스
class posts(db.Model):
    id=db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    p_title=db.Column(db.String(30), nullable=False)
    p_keyword=db.Column(db.String(30), nullable=False)
    p_price=db.Column(db.String(30), nullable=False)
    p_seller=db.Column(db.String(30), nullable=False)
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

# 팔로잉 데이터베이스
class follows(db.Model):
    id=db.Column(db.Integer, primary_key=True,unique=True,autoincrement=True)
    f_follower=db.Column(db.String(30), nullable=False)
    f_followee=db.Column(db.String(30), nullable=False)
    
    def __init__(self, follower, followee):
        self.f_follower=follower
        self.f_followee=followee

# 홈 화면 라우팅
@app.route('/')
def home():
    # 회원 가입에서 입력 값 유지에 사용하는 전역 변수
    global signUpId
    global signUpPassword
    global signUpNickname
    global isIdDuplicate
    global isNicknameDuplicate
    
    # 로그인에서 입력 값 유지에 사용하는 전역 변수
    global signInId
    global signInPassword
    
    # 판매 글 작성에서 입력 값 유지에 사용하는 전역 변수
    global registerTitle
    global registerPrice
    global registerDescription
    global registerimage1
    global registerimage2
    global registerimage3
    
    # 판매 글 수정에서 입력 값 유지 및 데이터베이스 업데이트에 사용하는 전역 변수
    global updateTitle
    global updatePrice
    global updateDescription
    global updateimage1
    global updateimage2
    global updateimage3
    
    # 홈에 오면 회원가입에 사용했던 값들을 초기화
    signUpId=''
    signUpPassword=''
    signUpNickname=''
    isIdDuplicate=True
    isNicknameDuplicate=True
    
    # 홈에 오면 로그인에 사용했던 값들을 초기화
    signInId=''
    signInPassword=''
    
    # 홈에 오면 판매 글 작성에 사용했던 값들을 초기화
    registerTitle=''
    registerPrice=''
    registerDescription=''
    registerimage1=''
    registerimage2=''
    registerimage3='' 
    
    # 홈에 오면 판매 글 수정에 사용했던 값들을 초기화
    updateTitle=''
    updatePrice=''
    updateDescription=''
    updateimage1=''
    updateimage2=''
    updateimage3='' 
    
    # 최종적으로 홈 화면을 랜더링
    return render_template('home.html')

# 회원가입 페이지에서 입력 값을 기억하는 변수들 선언
signUpId=''
signUpPassword=''
signUpNickname=''
isIdDuplicate=True
isNicknameDuplicate=True

# 회원 가입 라우팅
@app.route('/signUp/', methods=['GET', 'POST'])
def signUp():
    # 전역 변수 사용
    global signUpId
    global signUpPassword
    global signUpNickname
    global isIdDuplicate
    global isNicknameDuplicate
    
    # 요청이 POST이면
    if request.method=='POST':
        # 아이디, 비밀번호, 닉네임이 비어있으면
        if not request.form['a_id'] or not request.form['a_password'] or not request.form['a_nickname']:
            flash('아이디, 비밀번호, 닉네임 모두를 입력해주세요.', 'error')
            #입력했던 값 임시 저장
            signUpId=request.form['a_id']
            signUpPassword=request.form['a_password']
            signUpNickname=request.form['a_nickname']
        # 아이디 중복 확인을 하지 않았으면
        elif isIdDuplicate==True:
            flash('아이디 중복 확인을 해주세요.', 'error')
            #입력했던 값 임시 저장
            signUpId=request.form['a_id']
            signUpPassword=request.form['a_password']
            signUpNickname=request.form['a_nickname']
        # 닉네임 중복 확인을 하지 않았으면
        elif isNicknameDuplicate==True:
            flash('닉네임 중복 확인을 해주세요.', 'error')
            #입력했던 값 임시 저장
            signUpId=request.form['a_id']
            signUpPassword=request.form['a_password']
            signUpNickname=request.form['a_nickname']
        # 아이디 또는 닉네임의 중복 확인을 했으나 중복 확인 후 값을 바꿨다면
        elif request.form['a_id']!=signUpId or request.form['a_nickname']!=signUpNickname:
            flash('새로운 아이디 또는 새로운 닉네임을 입력하셨습니다. 중복 확인을 다시 해주세요.', 'error')
            #입력했던 값 임시 저장
            signUpId=request.form['a_id']
            signUpPassword=request.form['a_password']
            signUpNickname=request.form['a_nickname']
            isIdDuplicate==True
            isNicknameDuplicate==True
        # 문제가 없으면 회원 가입을 진행
        else:
            # 데이터베이스에 추가
            account=accounts(request.form['a_id'], request.form['a_password'], request.form['a_nickname'])
            db.session.add(account)
            db.session.commit()
            flash('회원가입을 성공했습니다.')
            #입력했던 값과 중복 여부 초기화
            signUpId=''
            signUpPassword=''
            signUpNickname=''
            isIdDuplicate=True
            isNicknameDuplicate=True
            # 홈으로 이동
            return redirect(url_for('home'))
    # GET이었거나 POST에서 회원가입을 완료하지 못했으면 현재까지 임시 저장된 입력 값을 이용해 다시 회원가입 화면 랜더링
    return render_template('signUp.html', id=signUpId, password=signUpPassword,nickname=signUpNickname)

# 아이디 중복 확인하는 라우팅(메서드)
@app.route('/idDuplicateCheck/', methods=['GET', 'POST'])
def idDuplicateCheck():
    global signUpId
    global signUpPassword
    global isIdDuplicate
    # 다시 랜더링 하기 위해 현재 비밀번호를 기억해둔다
    signUpPassword=request.form['a_password']
    
    if not request.form['a_id']:
        flash('아이디를 입력한 뒤 중복 확인을 해주세요.')
        return redirect(url_for('signUp'))
    
    if request.method=='POST':
        # 입력 아이디와 일치하는 아이디가 있는지 찾는다
        id=accounts.query.filter_by(a_id=request.form['a_id']).first()
        # 일치하는 것이 존재하면 새로운 아이디를 입력하게 한다
        if(id):
            flash('아이디가 이미 존재합니다. 다른 아이디를 입력해주세요.')
            
            signUpId =''
            isIdDuplicate=True
            return redirect(url_for('signUp'))
        # 일치하는 것이 존재하지 않으면 기존 입력 값을 이용해 랜더링하고 회원가입을 이어서 진행하게 한다
        else:
            flash('아이디가 존재하지 않습니다. 사용 가능합니다.')
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
        flash('닉네임을 입력한 뒤 중복 확인을 해주세요.')
        return redirect(url_for('signUp'))
    
    if request.method=='POST':
        # 입력 닉네임과 일치하는 닉네임이 있는지 찾는다
        nickname=accounts.query.filter_by(a_nickname=request.form['a_nickname']).first()
        # 일치하는 것이 존재하면 새로운 닉네임을 입력하게 한다
        if(nickname):
            flash('닉네임이 이미 존재합니다. 다른 닉네임을 입력해주세요.')
            
            signUpNickname =''
            isNicknameDuplicate=True
            return redirect(url_for('signUp'))
        # 일치하는 것이 존재하지 않으면 기존 입력 값을 이용해 랜더링하고 회원가입을 이어서 진행하게 한다
        else:
            flash('닉네임이 존재하지 않습니다. 사용 가능합니다.')
            signUpNickname=request.form['a_nickname']
            isNicknameDuplicate=False
            return redirect(url_for('signUp'))
        
# 로그인 시 입력 값을 임시 저장하는 변수     
signInId=''
signInPassword=''
# 로그인 라우팅
@app.route('/signIn/', methods=['GET', 'POST'])
def signIn():
    # 전역변수 사용
    global signInId
    global signInPassword
    # 요청이 'POST'이면
    if request.method=='POST':
        # id, password 중 빈 것이 있으면 입력을 유도하고 입력 값을 임시 저장한 뒤 다시 로그인 라우팅
        if not request.form['a_id'] or not request.form['a_password']:
            flash('아이디, 비밀번호 모두를 입력해주세요.', 'error')
            signInId=request.form['a_id']
            signInPassword=request.form['a_password']
            return redirect(url_for('signIn'))
        
        # id와 일치하는 계정을 찾는다
        account=accounts.query.filter_by(a_id=request.form['a_id']).first()
        # 일치하는 계정이 없으면 id가 존재하지 않음을 알리고 모든 입력 값을 초기화한 뒤 로그인 라우팅
        if not account:
            flash('존재하지 않는 아이디입니다.')
            signInId=''
            signInPassword=''
            return redirect(url_for('signIn'))
        # password가 일치하지 않은 경우, 입력 id는 저장하고 경고 메세지를 보여준 다음 로그인 라우팅
        elif account.a_password!=request.form['a_password']:
            signInId=request.form['a_id']
            signInPassword=''
            flash('비밀번호를 다시 확인해주세요.')
            return redirect(url_for('signIn'))
        # id가 존재하고 password가 일치한 경우, 입력 값을 초기화하고 로그인 세션 생성 후 홈페이지로 이동
        else:
            signInId=''
            signInPassword=''
            flash('로그인을 성공했습니다.')
            session['nickname']=account.a_nickname
            return redirect(url_for('home'))
    # 임시 저장된 입력 값을 이용하여 로그인 페이지를 랜더링
    return render_template('signIn.html', id=signInId,password=signInPassword)

# 로그아웃 라우팅
@app.route('/signOut/', methods=['GET', 'POST'])
def signOut():
    # 로그인 세션에서 닉네임을 꺼낸 뒤, 다시 홈으로 라우팅
    session.pop('nickname',None)
    flash('로그아웃을 성공했습니다.')
    return redirect(url_for('home'))

# 상품 등록에서 입력 값을 임시 저장하거나 파일을 저장하는데 사용되는 전역변수들
registerTitle=''
registerPrice=''
registerDescription=''
registerimage1=''
registerimage2=''
registerimage3='' 
# 상품 등록 라우팅
@app.route('/register/', methods=['GET','POST'])
def register():
    # 전역변수 사용
    global registerTitle
    global registerPrice
    global registerDescription
    global registerimage1
    global registerimage2
    global registerimage3
    
    # 로그인하지 않으면 사용 불가, 로그인 유도: 이 부분은 경고 라우팅을 새로 만들었고 html에서 조건에따라 실행하게 수정함
    #if 'nickname' not in session:
        #flash('you must sign in to register a product')
        #return redirect(url_for('signIn'))
    
    # 요청이 'POST'이면
    if request.method=='POST':
        # 제목, 가격, 키워드를 지정하지 않으면 입력 값을 임시 저장하고 경고 메세지        
        if not request.form['p_title'] or not request.form['p_price'] or request.form['p_keyword']=='키워드 *':
            flash('제목, 가격, 키워드는 필수로 작성해야합니다.')
            registerTitle=request.form['p_title']
            registerPrice=request.form['p_price']
            registerDescription=request.form['p_description']
        # 제목, 가격, 키워드를 입력했다면 이미지와 설명은 선택사항이므로 상품 등록 진행
        else:
            # 이미지가 있으면 서버에 저장하고 DB에는 파일명을 저장한다. 이미지가 없으면 파일 이름은 ''
            if request.files['p_image1']:
                f1=request.files['p_image1']
                registerimage1=secure_filename(f1.filename)
                f1.save(os.path.join(app.config['UPLOAD_FOLDER'],registerimage1))
            if request.files['p_image2']:
                f2=request.files['p_image2']
                registerimage2=secure_filename(f2.filename)
                f2.save(os.path.join(app.config['UPLOAD_FOLDER'],registerimage2))
            if request.files['p_image3']:
                f3=request.files['p_image3']
                registerimage3=secure_filename(f3.filename)
                f3.save(os.path.join(app.config['UPLOAD_FOLDER'],registerimage3))
            
            # 상품 등록을 위한 DB 생성
            post=posts(request.form['p_title'], request.form['p_price'], request.form['p_keyword'], request.form['p_description'], session['nickname'],
                       registerimage1,registerimage2,registerimage3)
            # DB에 추가
            db.session.add(post)
            db.session.commit()
            # 임시 저장 값 초기화
            registerTitle=''
            registerPrice=''
            registerDescription=''
            registerimage1=''
            registerimage2=''
            registerimage3='' 
            flash('상품 등록을 성공했습니다.')
            # 생성을 마치면 홈으로 이동
            return redirect(url_for('home'))
    # 생성을 제대로 마치지 못했거나 'GET'이면 임시 저장값을 이용해 재등록 유도
    return render_template('register.html', title=registerTitle, price=registerPrice, description=registerDescription)

# 검색 라우팅   
@app.route('/search/<keyword>', methods=['GET','POST'])
def search(keyword):
    # 매개변수가 'all'이라면
    if keyword=='all':
        # 전체 DB를 가져온다
        list=posts.query.all()
        # 검색에 해당하는 html에 결과를 넘겨주고 랜더링
        return render_template('search.html', list=list, keyword=keyword)
    # 매개변수가 어떤 키워드로 존재한다면
    elif keyword=='keyword':
        temp=request.form['searchBar']
        # 해당 키워드를 이용해 검색한다
        return redirect(url_for('search',keyword=temp))
    # 어떤 키워드를 이용해 검색했으면
    else:
        # 그 키워드가 기본 값이라면 경고 메세지를 보내고 우선 전체 상품을 보여준다.
        if keyword=='default':
            flash('키워드를 선택한 후, 검색해주세요.')
            return redirect(url_for('search',keyword='all'))
        # 기본 값이 아니라 실제 존재하는 키워드를 입력했다면 그에 해당하는 쿼리를 실행하여 결과를 반환한다.
        list=posts.query.filter_by(p_keyword=keyword)
        return render_template('search.html', list=list, keyword=keyword)
           
# 상세 페이지 라우팅  
@app.route('/detail/<id>', methods=['GET','POST'])
def detail(id):
    # id에 해당하는 DB를 가져온다.
    post=posts.query.filter_by(id=id).first()
    # 이를 이용해 상세 페이지를 랜더링한다.
    return render_template('detail.html', post=post) 

# 이미지 페이지 랜더링
@app.route('/image/<name>', methods=['GET','POST'])
def image(name):
    # 이미지의 이름을 기반으로 해당 이미지를 크게 볼 수 있는 이미지 페이지를 랜더링한다.
    return render_template('image.html', image=name)     

# 수정 페이지 랜더링
@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    # id에 해당하는 DB를 가져온다.
    post=posts.query.filter_by(id=id).first()
    # 이를 이용해 수정 페이지를 랜더링한다. 제목, 가격, 설명을 미리 입력해둔다.
    return render_template('edit.html', title=post.p_title, price=post.p_price, description=post.p_description,id=id) 

# 수정 과정에서 임시로 사용하는 전역변수들
updateTitle=''
updatePrice=''
updateDescription=''
updateimage1=''
updateimage2=''
updateimage3='' 
# 수정 과정
@app.route('/update/<id>', methods=['GET','POST'])
def update(id):
    # 전역변수 사용
    global updateTitle
    global updatePrice
    global updateDescription
    global updateimage1
    global updateimage2
    global updateimage3
    # 새로 수정하고자 하는 제목, 가격, 키워드가 비어있으면 경고 메세지 출력 후, 지금까지 입력 값으로 수정 페이지 랜더링
    if not request.form['p_title'] or not request.form['p_price'] or request.form['p_keyword']=='키워드 *':
            flash('제목, 가격, 키워드는 필수로 작성해야합니다.')
            updateTitle=request.form['p_title']
            updatePrice=request.form['p_price']
            updateDescription=request.form['p_description']
            return render_template('edit.html', title=updateTitle, price=updatePrice, description=updateDescription,id=id) 
    # 필수 요소가 제대로 입력되어 있다면
    else:
        # 이미지 유무에 따라 서버에 새로 이미지를 저장하고 파일명을 기억
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
        
        # 기존 DB를 가져와 업데이트
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
        # 임시로 사용한 전역변수는 초기화
        updateTitle=''
        updatePrice=''
        updateDescription=''
        updateimage1=''
        updateimage2=''
        updateimage3='' 
        flash('게시글 수정을 성공했습니다.')
        # 수정 결과를 확인할 수 있도록 상세 페이지 로드
        return redirect(url_for('detail',id=id))

# 판매 완료 과정
@app.route('/soldOut/<id>',methods=['GET','POST'])
def soldOut(id):
    # id로 DB 가져오기
    post=posts.query.filter_by(id=id).first()
    # 상태를 판매 완료로 수정하기
    post.p_soldOut=True
    db.session.commit()
    flash('상품의 상태를 판매 완료로 갱신했습니다.')
    # 수정 결과를 확인할 수 있도록 상세 페이지 로드
    return redirect(url_for('detail',id=id))

# 사용자별 상품 목록 라우팅
@app.route('/profile/<nickname>',methods=['GET','POST'])
def profile(nickname):
    # 판매자로 DB 가져오기
    list=posts.query.filter_by(p_seller=nickname)
    # 팔로잉 유무를 확인하기 위해 로그인한 사용자와의 관계를 DB 에서 가져오기
    follow=follows.query.filter_by(f_follower=session['nickname'],f_followee=nickname)
    # 결과를 이용해 프로필 페이지 랜더링
    return render_template('profile.html',list=list, nickname=nickname, follow=follow)

# 팔로우 페이지 라우팅
@app.route('/follow/<nickname>',methods=['GET','POST'])
def follow(nickname):
    # 팔로워의 닉네임을 이용해 DB 가져오기
    follow=follows.query.filter_by(f_follower=nickname)
    # 결과를 이용해 팔로잉 페이지 랜더링
    return render_template('follow.html', follow=follow)

# 팔로잉하는 과정
@app.route('/following/<nickname>',methods=['GET','POST'])
def following(nickname):
    # DB 생성후 추가
    follow=follows(session['nickname'], nickname)
    db.session.add(follow)
    db.session.commit()
    flash('팔로잉을 성공했습니다.')
    # 팔로잉 결과를 확인할 수 있도록 팔로우 페이지 로드
    return redirect(url_for('follow',nickname=session['nickname']))

# 로그인없이 사용할 경우에 대한 경고 과정
@app.route('/warning/<type>')
def warning(type):
    # 상품 등록에 대한 경고
    if type=='register':
        flash('상품 등록을 하기 위해 로그인이 필요합니다.')
    # 상품 목록 열람에 대한 경고
    elif type=='profile':
        flash('프로필 열람을 위해 로그인이 필요합니다.')
    # 팔로잉 열람에 대한 경고
    elif type=='follow':
        flash('팔로잉 보기를 위해 로그인이 필요합니다.')
    # 로그인 유도
    return redirect(url_for('signIn'))

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)

    