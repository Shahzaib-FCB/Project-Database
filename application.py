from cs50 import SQL
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_ECHO'] = True
bootstrap = Bootstrap(app)
database = SQLAlchemy(app)
db = SQL("sqlite:///DB-Proj.db")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(15), unique=True)
    email = database.Column(database.String(50), unique=True)
    password = database.Column(database.String(80))
    authority = database.Column(database.String(10))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route("/")
def index():
    feeDeadlines=db.execute("SELECT FeeDate, Sname, Cname, TotalAmount FROM School, Course, Fee WHERE Fee.SchRegNo=School.RegNo AND Course.CourseId=Fee.CourseId")
    testDeadlines=db.execute("SELECT TestDate, Centre, Cname, Sname FROM Test")
    return render_template("index.html",feeDeadlines=feeDeadlines, testDeadlines= testDeadlines, page="fee")

@app.route("/searchindex", methods=['POST'])
def searchindex():
    school=db.execute("SELECT RegNo, School.Sname, Location, PhoneNo, Website, CityRank FROM School, Rank WHERE Rank.SchRegNo = School.RegNo AND Location LIKE :search ORDER BY Rank.CityRank ASC", search='%'+request.form["search"] +'%')
    return render_template("index.html", school= school, page="location")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return "<h1>Wrong Username or Password</h1><h6>Remember Username is not the email ID</h6>"

    return render_template("login.html", form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, authority="user")
        database.session.add(new_user)
        database.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def dashboard():
    scholarships_per_city=db.execute("SELECT Location,COUNT(schName) AS Schools FROM School, Scholarship WHERE RegNo=schRegNo GROUP BY Location HAVING COUNT(schName)")
    school_per_city=db.execute("SELECT Location, COUNT(RegNo) AS number_of_Schools FROM School GROUP BY Location HAVING COUNT(RegNo)")
    courses_per_school=db.execute("SELECT Sname, COUNT(Cname) AS Courses FROM School, Course WHERE School.RegNo = Course.SchRegNo GROUP BY Sname HAVING COUNT(Cname)")
    courses_per_city=db.execute("SELECT City, COUNT(Cname) AS CoursespCity FROM School, Course, Location WHERE Course.SchRegNo = School.RegNo AND Location.SchRegNo = School.RegNo GROUP BY City HAVING COUNT(Cname)")
    return render_template("dashboard.html",school=school_per_city, scholarships=scholarships_per_city, coursesperSchool=courses_per_school, coursesperCity=courses_per_city, name=current_user.username)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contactUs")
def contactUs():
    return render_template("contactUs.html")

@app.route("/insertComment", methods=["POST"])
def insertComment():
    if request.form["firstname"] == "" or request.form["lastname"] == "" or request.form["comment"] == "":
        return "<h1>Enter your name and comment<h1>"
    db.execute("INSERT INTO Feedback(firstname, lastname, Location, comment) VALUES(:firstname, :lastname, :Location, :comment)", firstname=request.form["firstname"], lastname=request.form["lastname"], Location=request.form["Location"], comment=request.form["comment"])
    return "<h1>Comment Registered Sucessfully!<h1>"

# Gives options for update, view & Delete
@app.route("/school")
@login_required
def school():
    school=db.execute("SELECT Sname, Location FROM School")
    return render_template("school/school.html", school=school, authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/schoolInsert", methods=["GET","POST"])
@login_required
def schoolInsert():
    if request.method=="GET":
        return render_template("school/schoolInsert.html", name=current_user.username)
    elif request.method=="POST":
        if request.form["Sname"] == "" or request.form["Location"] == "":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO School(RegNo, Sname, Location, PhoneNo, Website) VALUES(:RegNo, :Sname, :Location, :PhoneNo, :Website)",
            RegNo=request.form["RegNo"], Sname=request.form["Sname"], Location=request.form["Location"], PhoneNo=request.form["PhoneNo"], Website=request.form["Website"])
        return redirect(url_for("schoolView"))

# deals with View of the table
@app.route("/schoolView")
@login_required
def schoolView():
    rows = db.execute("SELECT * FROM School")
    return render_template("school/schoolView.html", schoolView = rows, name=current_user.username)

@app.route("/searchschool", methods=["POST"])
def searchschool():
    rows=db.execute("SELECT * FROM School WHERE Location LIKE :search OR Sname LIKE :search", search='%'+request.form["search"] +'%')
    return render_template("school/schoolView.html", schoolView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/schoolDelete", methods= ["GET", "POST"])
@login_required
def schoolDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM School")
        return render_template("school/schoolDelete.html", schoolDelete= rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["RegNo"]:
            db.execute("DELETE FROM School WHERE RegNo = :RegNo",RegNo=request.form["RegNo"])
        return redirect(url_for("schoolView"))

# COURSE
# Gives options for update, view & Delete
@app.route("/course")
@login_required
def course():
    course=db.execute("SELECT Cname, Level, Sname FROM School, Course WHERE RegNo=SchRegNo")
    return render_template("course/course.html", course=course, authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/courseInsert", methods=["GET","POST"])
@login_required
def courseInsert():
    if request.method=="GET":
        rows = db.execute("SELECT RegNo, Sname FROM School")
        return render_template("course/courseInsert.html", InsCourse = rows, name=current_user.username)
    elif request.method=="POST":
        if request.form["CourseId"] == "" or request.form["Cname"] == "":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO Course(CourseId, Cname, Level, SchRegNo) VALUES(:CourseId, :Cname, :Level, :SchRegNo)",
            CourseId=request.form["CourseId"], Cname=request.form["Cname"], Level=request.form["Level"], SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("courseView"))

# deals with View of the table
@app.route("/courseView")
@login_required
def courseView():
    rows = db.execute("SELECT * FROM Course")
    return render_template("course/courseView.html", courseView = rows, name=current_user.username)

@app.route("/searchcourse", methods=["POST"])
def searchcourse():
    rows=db.execute("SELECT * FROM Course WHERE Cname LIKE :search OR Level LIKE :search", search='%'+request.form["search"] +'%')
    return render_template("course/courseView.html", courseView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/courseDelete", methods= ["GET", "POST"])
@login_required
def courseDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Course")
        return render_template("course/courseDelete.html", courseDelete= rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["CourseId"]:
            db.execute("DELETE FROM Course WHERE CourseId = :CourseId",CourseId=request.form["CourseId"])
        return redirect(url_for("courseView"))

# SCHOLARSHIP
# Gives options for update, view & Delete
@app.route("/scholarship")
@login_required
def scholarship():
    scholarship=db.execute("SELECT Type, OrgName, Sname, Amount FROM School, Scholarship WHERE RegNo=SchRegNo")
    return render_template("scholarship/scholarship.html",scholarship=scholarship, authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/scholarshipInsert", methods=["GET","POST"])
@login_required
def scholarshipInsert():
    if request.method=="GET":
        rows = db.execute("SELECT RegNo, Sname FROM School")
        return render_template("scholarship/scholarshipInsert.html", InsScholarship = rows, name=current_user.username)
    elif request.method=="POST":
        if request.form["schName"] == "" or request.form["OrgName"] == "":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO Scholarship(schName, OrgName, Type, Amount, SchRegNo) VALUES(:schName, :OrgName, :Type, :Amount, :SchRegNo)",
            schName=request.form["schName"], OrgName=request.form["OrgName"], Type=request.form["Type"], Amount=request.form["Amount"], SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("scholarshipView"))

# deals with View of the table
@app.route("/scholarshipView")
@login_required
def scholarshipView():
    rows = db.execute("SELECT * FROM Scholarship")
    return render_template("scholarship/scholarshipView.html", scholarshipView = rows, name=current_user.username)

@app.route("/searchscholarship", methods=["POST"])
def searchscholarship():
    rows=db.execute("SELECT * FROM scholarship WHERE schName LIKE :search OR OrgName LIKE :search OR Type LIKE :search", search='%'+request.form["search"] +'%')
    return render_template("scholarship/scholarshipView.html", scholarshipView = rows, name=current_user.username)

@app.route("/rangescholarship", methods=["POST"])
def rangescholarship():
    rows=db.execute("SELECT * FROM scholarship WHERE Amount BETWEEN :minimum AND :maximum", minimum=request.form["minimum"], maximum=request.form["maximum"])
    return render_template("scholarship/scholarshipView.html", scholarshipView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/scholarshipDelete", methods= ["GET", "POST"])
@login_required
def scholarshipDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Scholarship")
        return render_template("scholarship/scholarshipDelete.html", scholarshipDelete= rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["schName"]:
            db.execute("DELETE FROM Scholarship WHERE schName = :schName", schName=request.form["schName"])
        return redirect(url_for("scholarshipView"))

# ADMISSION
# Gives options for update, view & Delete
@app.route("/admission")
@login_required
def admission():
    admission=db.execute("SELECT Sname, Fee, MarksReq  FROM School, Admission WHERE RegNo=SchRegNo")
    return render_template("admission/admission.html",admission=admission, authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/admissionInsert", methods=["GET","POST"])
@login_required
def admissionInsert():
    if request.method=="GET":
        rows = db.execute("SELECT RegNo, Sname FROM School")
        return render_template("admission/admissionInsert.html", InsAdmission = rows, name=current_user.username)
    elif request.method=="POST":
        if request.form["SchRegNo"] == "":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO Admission(Fee, Level, MarksReq, SchRegNo) VALUES(:Fee, :Level, :MarksReq, :SchRegNo)",
            Fee=request.form["Fee"], Level=request.form["Level"], MarksReq=request.form["MarksReq"], SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("admissionView"))

# deals with View of the table
@app.route("/admissionView")
@login_required
def admissionView():
    rows = db.execute("SELECT * FROM Admission")
    return render_template("admission/admissionView.html", admissionView = rows, name=current_user.username)

@app.route("/rangeadmission", methods=["POST"])
def rangeadmission():
    rows=db.execute("SELECT * FROM admission WHERE Fee BETWEEN :minimum AND :maximum", minimum=request.form["minimum"], maximum=request.form["maximum"])
    return render_template("admission/admissionView.html", admissionView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/admissionDelete", methods= ["GET", "POST"])
@login_required
def admissionDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Admission")
        return render_template("admission/admissionDelete.html", admissionDelete= rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Admission WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("admissionView"))

# RESULT
# Gives options for update, view & Delete
@app.route("/result")
@login_required
def result():
    result=db.execute("SELECT Sname, Result.Location, PassPer, FailPer FROM Result, School WHERE RegNo=SchRegNo")
    return render_template("results/result.html", result=result,authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/resultInsert", methods=["GET","POST"])
@login_required
def resultInsert():
    if request.method=="GET":
        rows = db.execute("SELECT RegNo, Sname FROM School")
        return render_template("results/resultInsert.html", InsResult = rows, name=current_user.username)
    elif request.method=="POST":
        if request.form["SchRegNo"]=="":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO Result(Location, FailPer, PassPer, Level, SchRegNo) VALUES(:Location, :FailPer, :PassPer, :Level, :SchRegNo)",
            Location=request.form["Location"], FailPer=request.form["FailPer"], PassPer=request.form["PassPer"], Level=request.form["Level"], SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("resultView"))

# deals with View of the table
@app.route("/resultView")
@login_required
def resultView():
    rows = db.execute("SELECT * FROM Result")
    return render_template("results/resultView.html", resultView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/resultDelete", methods= ["GET", "POST"])
@login_required
def resultDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Result")
        return render_template("results/resultDelete.html", resultDelete= rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Result WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("resultView"))

# FEE
# Gives options for update, view & Delete
@app.route("/fee")
@login_required
def fee():
    fee=db.execute("SELECT Cname, Sname, TotalAmount, FeeDate FROM Fee, Course, School WHERE RegNo=Fee.SchRegNo AND Course.CourseId=Fee.CourseId")
    return render_template("fee/fee.html",fee=fee, authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/feeInsert", methods=["GET","POST"])
@login_required
def feeInsert():
    if request.method=="GET":
        School = db.execute("SELECT RegNo, Sname FROM School")
        Course = db.execute("SELECT CourseId, Cname FROM Course")
        return render_template("fee/feeInsert.html", InsSchoolFee = School, InsCourseFee = Course, name=current_user.username)
    elif request.method=="POST":
        if request.form["FeeId"] == "" or request.form["SchRegNo"] == "":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO Fee(FeeId, TotalAmount, Level, FeeDate, SchRegNo, CourseId) VALUES(:FeeId, :TotalAmount, :Level, :FeeDate, :SchRegNo, :CourseId)",
            FeeId=request.form["FeeId"], TotalAmount=request.form["TotalAmount"], Level=request.form["Level"], FeeDate=request.form["FeeDate"], SchRegNo=request.form["SchRegNo"], CourseId=request.form["CourseId"])
        return redirect(url_for("feeView"))

# deals with View of the table
@app.route("/feeView")
@login_required
def feeView():
    rows = db.execute("SELECT * FROM Fee")
    return render_template("fee/feeView.html", feeView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/feeDelete", methods= ["GET", "POST"])
@login_required
def feeDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Fee")
        return render_template("fee/feeDelete.html", feeDelete=rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["FeeId"]:
            db.execute("DELETE FROM Fee WHERE FeeId = :FeeId", FeeId=request.form["FeeId"])
        return redirect(url_for("feeView"))

# TEST
# Gives options for update, view & Delete
@app.route("/test")
@login_required
def test():
    test=db.execute("SELECT Cname, Sname, TestDate, Centre FROM Test")
    return render_template("test/test.html",test=test, authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/testInsert", methods=["GET","POST"])
@login_required
def testInsert():
    if request.method=="GET":
        rows = db.execute("SELECT RegNo, Sname FROM School")
        return render_template("test/testInsert.html", InsTest = rows, name=current_user.username)
    elif request.method=="POST":
        if request.form["TestDate"] == "" or request.form["Level"] == "" or request.form["Centre"] == "" or request.form["Cname"] == "" or request.form["Sname"] == "" or request.form["SchRegNo"] == "":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO Test(TestDate, Level, Centre, Cname, Sname, SchRegNo) VALUES(:TestDate, :Level, :Centre, :Cname, :Sname, :SchRegNo)",
            TestDate=request.form["TestDate"], Level=request.form["Level"], Centre=request.form["Centre"], Cname=request.form["Cname"], Sname=request.form["Sname"], SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("testView"))

# deals with View of the table
@app.route("/testView")
@login_required
def testView():
    rows = db.execute("SELECT * FROM Test")
    return render_template("test/testView.html", testView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/testDelete", methods= ["GET", "POST"])
@login_required
def testDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Test")
        return render_template("test/testDelete.html", testDelete=rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Test WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("testView"))

# LOCATION
# Gives options for update, view & Delete
@app.route("/location")
@login_required
def location():
    location=db.execute("SELECT Sname, City, District, Province FROM Location")
    return render_template("location/location.html",location=location, authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/locationInsert", methods=["GET","POST"])
@login_required
def locationInsert():
    if request.method=="GET":
        rows = db.execute("SELECT RegNo, Sname FROM School")
        return render_template("location/locationInsert.html", InsLocation = rows, name=current_user.username)
    elif request.method=="POST":
        if request.form["Sname"] == "" or request.form["District"] == "" or request.form["Province"] == "" or request.form["SchRegNo"] == "":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO Location(Sname, City, CampusName, District, Province, SchRegNo) VALUES(:Sname, :City, :CampusName, :District, :Province, :SchRegNo)",
            Sname=request.form["Sname"], City=request.form["City"], CampusName=request.form["CampusName"], District=request.form["District"], Province=request.form["Province"], SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("locationView"))

# deals with View of the table
@app.route("/locationView")
@login_required
def locationView():
    rows = db.execute("SELECT * FROM Location")
    return render_template("location/locationView.html", locationView = rows, name=current_user.username)

@app.route("/searchlocation", methods=["POST"])
def searchlocation():
    rows=db.execute("SELECT * FROM Location WHERE City LIKE :search OR Sname LIKE :search OR Province LIKE :search", search='%'+request.form["City"] +'%')
    return render_template("location/locationView.html", locationView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/locationDelete", methods= ["GET", "POST"])
@login_required
def locationDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Location")
        return render_template("location/locationDelete.html", locationDelete= rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Location WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("locationView"))

# RANK
# Gives options for update, view & Delete
@app.route("/rank")
@login_required
def rank():
    rank=db.execute("SELECT Sname, DistrictRank, CityRank FROM Rank")
    return render_template("rank/rank.html",rank=rank, authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/rankInsert", methods=["GET","POST"])
@login_required
def rankInsert():
    if request.method == "GET":
        Insrows = db.execute("SELECT RegNo, Sname FROM School")
        return render_template("rank/rankInsert.html", InsRank = Insrows, name=current_user.username)
    elif request.method == "POST":
        if request.form["Sname"] == "" or request.form["DistrictRank"] == "" or request.form["SchRegNo"] == "":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO Rank(Sname, DistrictRank, CityRank, SchRegNo) VALUES(:Sname, :DistrictRank, :CityRank, :SchRegNo)",
            Sname=request.form["Sname"], DistrictRank=request.form["DistrictRank"], CityRank=request.form["CityRank"], SchRegNo=request.form["SchRegNo"])
        rows = db.execute("SELECT * FROM Rank")
        return redirect(url_for("rankView"))

# deals with View of the table
@app.route("/rankView")
@login_required
def rankView():
    rows = db.execute("SELECT * FROM Rank")
    return render_template("rank/rankView.html", rankView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/rankDelete", methods= ["GET", "POST"])
@login_required
def rankDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Rank")
        return render_template("rank/rankDelete.html", rankDelete= rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Rank WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("rankView"))

# COUNCELLINGCENTRE
# Gives options for update, view & Delete
@app.route("/centre")
@login_required
def centre():
    centre=db.execute("SELECT Name, Adress FROM CounsellingCentres")
    return render_template("counsellingCentre/centre.html",centre=centre, authority=current_user.authority, name=current_user.username)

# deals with updation of the table
@app.route("/centreInsert", methods=["GET","POST"])
@login_required
def centreInsert():
    if request.method == "GET":
        return render_template("counsellingCentre/centreInsert.html", name=current_user.username)
    elif request.method == "POST":
        if request.form["Name"] == "" or request.form["Adress"] == "":
            return render_template("failure.html", name=current_user.username)
        db.execute("INSERT INTO CounsellingCentres(Name, Adress, PhoneNumber) VALUES(:Name, :Adress, :PhoneNumber)",
            Name=request.form["Name"], Adress=request.form["Adress"], PhoneNumber=request.form["PhoneNumber"])
        return redirect(url_for("centreView"))

# deals with View of the table
@app.route("/centreView")
@login_required
def centreView():
    rows = db.execute("SELECT * FROM CounsellingCentres")
    return render_template("counsellingCentre/centreView.html", centreView = rows, name=current_user.username)

# deals with Deletion of the table
@app.route("/centreDelete", methods= ["GET", "POST"])
@login_required
def centreDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM CounsellingCentres")
        return render_template("counsellingCentre/centreDelete.html", centreDelete= rows, name=current_user.username)
    elif request.method == "POST":
        if request.form["Name"]:
            db.execute("DELETE FROM CounsellingCentres WHERE Name = :Name", Name=request.form["Name"])
        return redirect(url_for("centreView"))