from cs50 import SQL
from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

db = SQL("sqlite:///DB-Proj.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contactUs")
def contactUs():
    return render_template("contactUs.html")

# Gives options for update, view & Delete
@app.route("/school")
def school():
    return render_template("school/School.html")

# Handles the url
@app.route("/handleSchool", methods=["POST", "GET"])
def handleSchool():
    if request.form["button"] == "schoolView":
        return redirect(url_for("schoolView"))
    elif request.form["button"] == "schoolDelete":
        return redirect(url_for("schoolDelete"))
    elif request.form["button"] == "InsSchool":
        return redirect(url_for("InsSchool"))

# renders a new html file
@app.route("/InsSchool")
def InsSchool():
    return render_template("school/InsSchool.html")

# deals with updation of the table
@app.route("/schoolInsert", methods=["POST"])
def schoolInsert():
    if request.form["Sname"] == "" or request.form["Location"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO School(RegNo, Sname, Location, PhoneNo, Website) VALUES(:RegNo, :Sname, :Location, :PhoneNo, :Website)",
        RegNo=request.form["RegNo"], Sname=request.form["Sname"], Location=request.form["Location"], PhoneNo=request.form["PhoneNo"], Website=request.form["Website"])
    return render_template("success.html")

# deals with View of the table
@app.route("/schoolView")
def schoolView():
    rows = db.execute("SELECT * FROM School")
    return render_template("school/schoolView.html", schoolView = rows)

# deals with Deletion of the table
@app.route("/schoolDelete", methods= ["GET", "POST"])
def schoolDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM School")
        return render_template("school/schoolDelete.html", schoolDelete= rows)
    elif request.method == "POST":
        if request.form["RegNo"]:
            db.execute("DELETE FROM School WHERE RegNo = :RegNo",RegNo=request.form["RegNo"])
        return redirect(url_for("schoolView"))

# COURSE
# Gives options for update, view & Delete
@app.route("/course")
def course():
    return render_template("courses/Course.html")

# Handles the url
@app.route("/handleCourse", methods=["POST", "GET"])
def handleCourse():
    if request.form["button"] == "courseView":
        return redirect(url_for("courseView"))
    elif request.form["button"] == "courseDelete":
        return redirect(url_for("courseDelete"))
    elif request.form["button"] == "InsCourse":
        return redirect(url_for("InsCourse"))

# renders a new html file
@app.route("/InsCourse")
def InsCourse():
    rows = db.execute("SELECT RegNo, Sname FROM School")
    return render_template("courses/InsCourse.html", InsCourse = rows)

# deals with updation of the table
@app.route("/courseInsert", methods=["POST"])
def courseInsert():
    if request.form["CourseId"] == "" or request.form["Cname"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO Course(CourseId, Cname, Level, SchRegNo) VALUES(:CourseId, :Cname, :Level, :SchRegNo)",
        CourseId=request.form["CourseId"], Cname=request.form["Cname"], Level=request.form["Level"], SchRegNo=request.form["SchRegNo"])
    return render_template("success.html")

# deals with View of the table
@app.route("/courseView")
def courseView():
    rows = db.execute("SELECT * FROM Course")
    return render_template("courses/courseView.html", courseView = rows)

# deals with Deletion of the table
@app.route("/courseDelete", methods= ["GET", "POST"])
def courseDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Course")
        return render_template("courses/courseDelete.html", courseDelete= rows)
    elif request.method == "POST":
        if request.form["CourseId"]:
            db.execute("DELETE FROM Course WHERE CourseId = :CourseId",CourseId=request.form["CourseId"])
        return redirect(url_for("courseView"))

# SCHOLARSHIP
# Gives options for update, view & Delete
@app.route("/scholarship")
def scholarship():
    return render_template("scholarships/scholarship.html")

# Handles the url
@app.route("/handleScholarship", methods=["POST", "GET"])
def handleScholarship():
    if request.form["button"] == "scholarshipView":
        return redirect(url_for("scholarshipView"))
    elif request.form["button"] == "scholarshipDelete":
        return redirect(url_for("scholarshipDelete"))
    elif request.form["button"] == "InsScholarship":
        return redirect(url_for("InsScholarship"))

# renders a new html file
@app.route("/InsScholarship")
def InsScholarship():
    rows = db.execute("SELECT RegNo, Sname FROM School")
    return render_template("scholarships/InsScholarship.html", InsScholarship = rows)

# deals with updation of the table
@app.route("/scholarshipInsert", methods=["POST"])
def scholarshipInsert():
    if request.form["schName"] == "" or request.form["OrgName"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO Scholarship(schName, OrgName, Type, Amount, SchRegNo) VALUES(:schName, :OrgName, :Type, :Amount, :SchRegNo)",
        schName=request.form["schName"], OrgName=request.form["OrgName"], Type=request.form["Type"], Amount=request.form["Amount"], SchRegNo=request.form["SchRegNo"])
    return render_template("success.html")

# deals with View of the table
@app.route("/scholarshipView")
def scholarshipView():
    rows = db.execute("SELECT * FROM Scholarship")
    return render_template("scholarships/scholarshipView.html", scholarshipView = rows)

# deals with Deletion of the table
@app.route("/scholarshipDelete", methods= ["GET", "POST"])
def scholarshipDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Scholarship")
        return render_template("scholarships/scholarshipDelete.html", scholarshipDelete= rows)
    elif request.method == "POST":
        if request.form["schName"]:
            db.execute("DELETE FROM Scholarship WHERE schName = :schName", schName=request.form["schName"])
        return redirect(url_for("scholarshipView"))

# ADMISSION
# Gives options for update, view & Delete
@app.route("/admission")
def admission():
    return render_template("admissions/admission.html")

# Handles the url
@app.route("/handleAdmission", methods=["POST", "GET"])
def handleAdmission():
    if request.form["button"] == "admissionView":
        return redirect(url_for("admissionView"))
    elif request.form["button"] == "admissionDelete":
        return redirect(url_for("admissionDelete"))
    elif request.form["button"] == "InsAdmission":
        return redirect(url_for("InsAdmission"))

# renders a new html file
@app.route("/InsAdmission")
def InsAdmission():
    rows = db.execute("SELECT RegNo, Sname FROM School")
    return render_template("admissions/InsAdmission.html", InsAdmission = rows)

# deals with updation of the table
@app.route("/admissionInsert", methods=["POST"])
def admissionInsert():
    if request.form["SchRegNo"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO Admission(Fee, Level, MarksReq, SchRegNo) VALUES(:Fee, :Level, :MarksReq, :SchRegNo)",
        Fee=request.form["Fee"], Level=request.form["Level"], MarksReq=request.form["MarksReq"], SchRegNo=request.form["SchRegNo"])
    return render_template("success.html")

# deals with View of the table
@app.route("/admissionView")
def admissionView():
    rows = db.execute("SELECT * FROM Admission")
    return render_template("admissions/admissionView.html", admissionView = rows)

# deals with Deletion of the table
@app.route("/admissionDelete", methods= ["GET", "POST"])
def admissionDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Admission")
        return render_template("admissions/admissionDelete.html", admissionDelete= rows)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Admission WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("admissionView"))

# RESULT
# Gives options for update, view & Delete
@app.route("/result")
def result():
    return render_template("results/result.html")

# Handles the url
@app.route("/handleResult", methods=["POST", "GET"])
def handleResult():
    if request.form["button"] == "resultView":
        return redirect(url_for("resultView"))
    elif request.form["button"] == "resultDelete":
        return redirect(url_for("resultDelete"))
    elif request.form["button"] == "InsResult":
        return redirect(url_for("InsResult"))

# renders a new html file
@app.route("/InsResult")
def InsResult():
    rows = db.execute("SELECT RegNo, Sname FROM School")
    return render_template("results/InsResult.html", InsResult = rows)

# deals with updation of the table
@app.route("/resultInsert", methods=["POST"])
def resultInsert():
    if request.form["SchRegNo"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO Result(Location, FailPer, PassPer, Level, SchRegNo) VALUES(:Location, :FailPer, :PassPer, :Level, :SchRegNo)",
        Location=request.form["Location"], FailPer=request.form["FailPer"], PassPer=request.form["PassPer"], Level=request.form["Level"], SchRegNo=request.form["SchRegNo"])
    return render_template("success.html")

# deals with View of the table
@app.route("/resultView")
def resultView():
    rows = db.execute("SELECT * FROM Result")
    return render_template("results/resultView.html", resultView = rows)

# deals with Deletion of the table
@app.route("/resultDelete", methods= ["GET", "POST"])
def resultDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Result")
        return render_template("results/resultDelete.html", resultDelete= rows)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Result WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("resultView"))

# FEE
# Gives options for update, view & Delete
@app.route("/fee")
def fee():
    return render_template("fee/fee.html")

# Handles the url
@app.route("/handleFee", methods=["POST", "GET"])
def handleFee():
    if request.form["button"] == "feeView":
        return redirect(url_for("feeView"))
    elif request.form["button"] == "feeDelete":
        return redirect(url_for("feeDelete"))
    elif request.form["button"] == "InsFee":
        return redirect(url_for("InsFee"))

# renders a new html file
@app.route("/InsFee")
def InsFee():
    School = db.execute("SELECT RegNo, Sname FROM School")
    Course = db.execute("SELECT CourseId, Cname FROM Course")
    return render_template("fee/InsFee.html", InsSchoolFee = School, InsCourseFee = Course)

# deals with updation of the table
@app.route("/feeInsert", methods=["POST"])
def feeInsert():
    if request.form["FeeId"] == "" or request.form["SchRegNo"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO Fee(FeeId, TotalAmount, Level, FeeDate, SchRegNo, CourseId) VALUES(:FeeId, :TotalAmount, :Level, :FeeDate, :SchRegNo, :CourseId)",
        FeeId=request.form["FeeId"], TotalAmount=request.form["TotalAmount"], Level=request.form["Level"], FeeDate=request.form["FeeDate"], SchRegNo=request.form["SchRegNo"], CourseId=request.form["CourseId"])
    return render_template("success.html")

# deals with View of the table
@app.route("/feeView")
def feeView():
    rows = db.execute("SELECT * FROM Fee")
    return render_template("fee/feeView.html", feeView = rows)

# deals with Deletion of the table
@app.route("/feeDelete", methods= ["GET", "POST"])
def feeDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Fee")
        return render_template("fee/feeDelete.html", feeDelete=rows)
    elif request.method == "POST":
        if request.form["FeeId"]:
            db.execute("DELETE FROM Fee WHERE FeeId = :FeeId", FeeId=request.form["FeeId"])
        return redirect(url_for("feeView"))

# TEST
# Gives options for update, view & Delete
@app.route("/test")
def test():
    return render_template("test/test.html")

# Handles the url
@app.route("/handleTest", methods=["POST", "GET"])
def handleTest():
    if request.form["button"] == "testView":
        return redirect(url_for("testView"))
    elif request.form["button"] == "testDelete":
        return redirect(url_for("testDelete"))
    elif request.form["button"] == "InsTest":
        return redirect(url_for("InsTest"))

# renders a new html file
@app.route("/InsTest")
def InsTest():
    rows = db.execute("SELECT RegNo, Sname FROM School")
    return render_template("test/InsTest.html", InsTest = rows)

# deals with updation of the table
@app.route("/testInsert", methods=["POST"])
def testInsert():
    if request.form["TestDate"] == "" or request.form["Level"] == "" or request.form["Centre"] == "" or request.form["Cname"] == "" or request.form["Sname"] == "" or request.form["SchRegNo"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO Test(TestDate, Level, Centre, Cname, Sname, SchRegNo) VALUES(:TestDate, :Level, :Centre, :Cname, :Sname, :SchRegNo)",
        TestDate=request.form["TestDate"], Level=request.form["Level"], Centre=request.form["Centre"], Cname=request.form["Cname"], Sname=request.form["Sname"], SchRegNo=request.form["SchRegNo"])
    return render_template("success.html")

# deals with View of the table
@app.route("/testView")
def testView():
    rows = db.execute("SELECT * FROM Test")
    return render_template("test/testView.html", testView = rows)

# deals with Deletion of the table
@app.route("/testDelete", methods= ["GET", "POST"])
def testDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Test")
        return render_template("test/testDelete.html", testDelete=rows)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Test WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("testView"))

# LOCATION
# Gives options for update, view & Delete
@app.route("/location")
def location():
    return render_template("location/location.html")

# Handles the url
@app.route("/handleLocation", methods=["POST", "GET"])
def handleLocation():
    if request.form["button"] == "locationView":
        return redirect(url_for("locationView"))
    elif request.form["button"] == "locationDelete":
        return redirect(url_for("locationDelete"))
    elif request.form["button"] == "InsLocation":
        return redirect(url_for("InsLocation"))

# renders a new html file
@app.route("/InsLocation")
def InsLocation():
    rows = db.execute("SELECT RegNo, Sname FROM School")
    return render_template("location/InsLocation.html", InsLocation = rows)

# deals with updation of the table
@app.route("/locationInsert", methods=["POST"])
def locationInsert():
    if request.form["Sname"] == "" or request.form["District"] == "" or request.form["Province"] == "" or request.form["SchRegNo"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO Location(Sname, City, CampusName, District, Province, SchRegNo) VALUES(:Sname, :City, :CampusName, :District, :Province, :SchRegNo)",
        Sname=request.form["Sname"], City=request.form["City"], CampusName=request.form["CampusName"], District=request.form["District"], Province=request.form["Province"], SchRegNo=request.form["SchRegNo"])
    return render_template("success.html")

# deals with View of the table
@app.route("/locationView")
def locationView():
    rows = db.execute("SELECT * FROM Location")
    return render_template("location/locationView.html", locationView = rows)

# deals with Deletion of the table
@app.route("/locationDelete", methods= ["GET", "POST"])
def locationDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Location")
        return render_template("location/locationDelete.html", locationDelete= rows)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Location WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("locationView"))

# RANK
# Gives options for update, view & Delete
@app.route("/rank")
def rank():
    return render_template("rank/rank.html")

# Handles the url
@app.route("/handleRank", methods=["POST", "GET"])
def handleRank():
    if request.form["button"] == "rankView":
        return redirect(url_for("rankView"))
    elif request.form["button"] == "rankDelete":
        return redirect(url_for("rankDelete"))
    elif request.form["button"] == "InsRank":
        return redirect(url_for("InsRank"))

# renders a new html file
@app.route("/InsRank")
def InsRank():
    rows = db.execute("SELECT RegNo, Sname FROM School")
    return render_template("rank/InsRank.html", InsRank = rows)

# deals with updation of the table
@app.route("/rankInsert", methods=["POST"])
def rankInsert():
    if request.form["Sname"] == "" or request.form["DistrictRank"] == "" or request.form["SchRegNo"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO Rank(Sname, DistrictRank, CityRank, SchRegNo) VALUES(:Sname, :DistrictRank, :CityRank, :SchRegNo)",
        Sname=request.form["Sname"], DistrictRank=request.form["DistrictRank"], CityRank=request.form["CityRank"], SchRegNo=request.form["SchRegNo"])
    return render_template("success.html")

# deals with View of the table
@app.route("/rankView")
def rankView():
    rows = db.execute("SELECT * FROM Rank")
    return render_template("rank/rankView.html", rankView = rows)

# deals with Deletion of the table
@app.route("/rankDelete", methods= ["GET", "POST"])
def rankDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM Rank")
        return render_template("rank/rankDelete.html", rankDelete= rows)
    elif request.method == "POST":
        if request.form["SchRegNo"]:
            db.execute("DELETE FROM Rank WHERE SchRegNo = :SchRegNo", SchRegNo=request.form["SchRegNo"])
        return redirect(url_for("rankView"))

# COUNCELLINGCENTRE
# Gives options for update, view & Delete
@app.route("/centre")
def centre():
    return render_template("counsellingCentres/centre.html")

# Handles the url
@app.route("/handleCentre", methods=["POST", "GET"])
def handleCentre():
    if request.form["button"] == "centreView":
        return redirect(url_for("centreView"))
    elif request.form["button"] == "centreDelete":
        return redirect(url_for("centreDelete"))
    elif request.form["button"] == "InsCentre":
        return redirect(url_for("InsCentre"))

# renders a new html file
@app.route("/InsCentre")
def InsCentre():
    return render_template("counsellingCentres/InsCentre.html")

# deals with updation of the table
@app.route("/centreInsert", methods=["POST"])
def centreInsert():
    if request.form["Name"] == "" or request.form["Adress"] == "":
        return render_template("failure.html")
    db.execute("INSERT INTO CounsellingCentres(Name, Adress, PhoneNumber) VALUES(:Name, :Adress, :PhoneNumber)",
        Name=request.form["Name"], Adress=request.form["Adress"], PhoneNumber=request.form["PhoneNumber"])
    return render_template("success.html")

# deals with View of the table
@app.route("/centreView")
def centreView():
    rows = db.execute("SELECT * FROM CounsellingCentres")
    return render_template("counsellingCentres/centreView.html", centreView = rows)

# deals with Deletion of the table
@app.route("/centreDelete", methods= ["GET", "POST"])
def centreDelete():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM CounsellingCentres")
        return render_template("counsellingCentres/centreDelete.html", centreDelete= rows)
    elif request.method == "POST":
        if request.form["Name"]:
            db.execute("DELETE FROM CounsellingCentres WHERE Name = :Name", Name=request.form["Name"])
        return redirect(url_for("centreView"))