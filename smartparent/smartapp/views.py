from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect,redirect
from datetime import date, datetime
today=date.today()

# Create your views here.
def index(request):
    return render(request,'index.html')
def ureg(request):
    return render(request,'ureg.html')
def dreg(request):
    return render(request,'dreg.html')
def login(request):
    return render(request,'login.html')
def userhome(request):
    return render(request,'userhome.html')
def adminhome(request):
    return render(request,'adminhome.html')
def doctorhome(request):
    return render(request,'doctorhome.html')
def useraction(request):
    cursor=connection.cursor()
    childname=request.GET['child']
    dob=request.GET['dob']
    sex=request.GET['sex']
    parentname=request.GET['parent']
    address=request.GET['address']
    city=request.GET['city']
    pincode=request.GET['pincode']
    phno=request.GET['phno']
    email=request.GET['email']
    password=request.GET['password']
    sql="insert into ureg(childname,dob,sex,parentname,address,city,pincode,phn,email)values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(childname,dob,sex,parentname,address,city,pincode,phno,email)
    cursor.execute(sql)
    s3="select max(userid) as userid from ureg"
    cursor.execute(s3)
    userresult=cursor.fetchall()
    for row in userresult:
        s4="insert into login(uid,username,password,type) values('%s','%s','%s','user')"%(row[0],email,password)
        cursor.execute(s4)
    msg="<script>alert('Added');window.location='/login/'</script>"
    return HttpResponse(msg)
def loginaction(request):
    cursor=connection.cursor()
    username=request.GET['email']
    password=request.GET['password']

    s5="select * from login where username='%s' and password='%s'" %(username,password)
    cursor.execute(s5)
    if cursor.rowcount>0:
        loginresult=cursor.fetchall()
        for row in loginresult:
            request.session['uid']=row[1]
            request.session['type']=row[4]
            request.session['status']=row[5]

        if request.session['type']=="admin":
            return render(request,'adminhome.html')
        elif request.session['type']=="user":
            return render(request,'userhome.html')
        elif request.session['type']=="Doctor" and request.session['status'] == "approved":
            return render(request,'doctorhome.html')
        elif request.session['type']=="Counsellor" and request.session['status'] == "approved":
            return render(request,'counsellorhome.html')
    else:
        msg="<script>alert('Invaild username or password');window.location='/login/'</script>"
        return HttpResponse(msg)
def userview(request):
    cursor=connection.cursor()
    s6="select * from ureg"
    cursor.execute(s6)
    userviewresult=cursor.fetchall()
    userlist=[]
    for row in userviewresult:
        q={'userid':row[0],'childname':row[1],'dob':row[2],'sex':row[3],'parentname':row[4],'address':row[5],'city':row[6],'pincode':row[7],'phn':row[8],'email':row[9]}
        userlist.append(q)
    return render(request,'userview.html',{'userlist':userlist})
def dregaction(request):
    cursor=connection.cursor()
    dname=request.GET['dname']
    dob=request.GET['dob']
    sex=request.GET['sex']
    address=request.GET['address']
    city=request.GET['city']
    pincode=request.GET['pincode']
    type=request.GET['type']
    qualification=request.GET['qualification']
    exp=request.GET['exp']
    phno=request.GET['phno']
    email=request.GET['email']
    password=request.GET['password']
    sql="insert into doctor(name,dob,sex,address,city,pincode,qualification,exp,phno,email,type)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(dname,dob,sex,address,city,pincode,qualification,exp,phno,email,type)
    cursor.execute(sql)
    s3="select max(doctorid) as doctorid from doctor"
    cursor.execute(s3)
    userresult=cursor.fetchall()
    for row in userresult:
        s4="insert into login(uid,username,password,type,status) values('%s','%s','%s','%s','%s')"%(row[0],email,password,type,'pending')
        cursor.execute(s4)
    msg="<script>alert('Added');window.location='/login/'</script>"
    return HttpResponse(msg)
            
     
def viewdoctor(request):
    cursor=connection.cursor()
    s6="select * from doctor inner join login on doctor.doctorid=login.uid where login.type='Doctor' or login.type='Counsellor'"
    cursor.execute(s6)
    doctorviewresult=cursor.fetchall()
    doctorlist=[]
    for row in doctorviewresult:
        q={'doctorid':row[0],'name':row[1],'dob':row[2],'sex':row[3],'address':row[4],'city':row[5],'pincode':row[6],'qualification':row[8],'exp':row[9],'phno':row[10],'email':row[11],'type':row[12],'uid':row[13],'username':row[14],'password':row[15],'type':row[16],'status':row[17]}
        doctorlist.append(q)
    return render(request,'viewdoctor.html',{'doctorlist':doctorlist})
def accept(request):
    cur=connection.cursor()
    id=request.GET['id']
    sql="update login set status='approved' where uid='%s' and (type='Doctor' or type='Counsellor') "%(id)
    cur.execute(sql)
    msg="<script>alert('Status updated');window.location='/viewdoctor/'</script>"
    return HttpResponse(msg)
def reject(request):
    cur=connection.cursor()
    id=request.GET['rid']
    sql="update login set status='Rejected' where uid='%s' and (type='Doctor' or type='Counsellor')"%(id)
    cur.execute(sql)
    msg="<script>alert('Status updated');window.location='/viewdoctor/'</script>"
    return HttpResponse(msg)
def dprofile(request):
    cur=connection.cursor()
    # oid=request.GET['id']
    uid=request.session['uid']
    s="select*from doctor where doctorid='%s'"%(uid)
    print(s)
    cur.execute(s)
    rs=cur.fetchall()
    cr=[]
    for row in rs:
        m={'doctorid':row[0],'name':row[1],'dob':row[2],'sex':row[3],'address':row[4],'city':row[5],'pincode':row[6],'qualification':row[7],'exp':row[8],'phno':row[9],'email':row[10],'type':row[11]}
        cr.append(m)
        return render(request,'dprofile.html',{'cr':cr})
def updatedprofile(request):
        cur=connection.cursor()
        uid=request.session['uid']
        sn=request.GET['name']
        sd=request.GET['dateofbirth']
        ss=request.GET['sex']
        sa=request.GET['address']
        sc=request.GET['city']
        sp=request.GET['pincode']
        sq=request.GET['qualification']
        se=request.GET['experince']
        sph=request.GET['phoneno']
        sm=request.GET['email']
        s = "update doctor set name='%s',dob='%s',sex='%s',address='%s',city='%s',pincode='%s',qualification='%s',exp='%s',phno='%s',email='%s' where doctorid='%s'" % (sn, sd, ss, sa, sc, sp, sq, se, sph, sm,uid)
        cur.execute(s)
        msg="<script>alert('Successfully Updated'); window.location='/doctorhome/';</script>"
        return HttpResponse(msg)
def questions(request):
    return render(request,'questions.html')
def addquestions(request):
    cursor=connection.cursor()
    s= "select * from addquestions"
    cursor.execute(s)
    result=cursor.fetchall()
    cursor=[]
    for row in result:
        q={'qid':row[0],'questions':row[1],'answer1':row[2],'answer2':row[3],'answer3':row[4]}
        cursor.append(q)
    return render(request,'addquestions.html',{'cursor':cursor})
# def addquestionaction(request):
#     cursor=connection.cursor()
#     questions=request.GET['a']
#     answer1=request.GET['Option1']
#     answer2=request.GET['Option2']
#     # answer3=request.GET['Option3']
#     sql="insert into addquestions(questions,answer1,answer2)values('%s','%s','%s')"%(questions,answer1,answer2)
#     cursor.execute(sql)
#     msg="<script>alert('Added');window.location='/addquestions/'</script>"
    # return HttpResponse(msg)
def delquestions(request):
    cursor=connection.cursor()
    qid=request.GET['id']
    sql="delete from addquestions where qid='%s'"%(qid)
    cursor.execute(sql)
    msg="<script>alert('Deleted sccessfully');window.location='/addquestions/'</script>"
    return HttpResponse(msg)
def personascan(request):
    cursor=connection.cursor()
    s= "select * from addquestions"
    cursor.execute(s)
    result=cursor.fetchall()
    cursor=[]
    for row in result:
        q={'qid':row[0],'questions':row[1],'answer1':row[2],'answer2':row[3]}
        cursor.append(q)
    return render(request,'personascan.html',{'cursor':cursor})


def peraction(request):
    cursor = connection.cursor()
    answer1 = request.GET['ans1']
    answer2 = request.GET['ans2']
    answer3 = request.GET['ans3']
    answer4 = request.GET['ans4']
    answer5 = request.GET['ans5']
    uid = request.session['uid']
   
    sql = "INSERT INTO addquestions (answer, answer1, answer2, answer3, answer4,uid) VALUES (%s, %s, %s, %s, %s,%s)"
    cursor.execute(sql, (answer1, answer2, answer3, answer4,answer5, uid))
    msg = "<script>alert('Added');window.location='/prediction/'</script>"
    return HttpResponse(msg)


def prediction(request):
    uid = request.session['uid']
    cursor = connection.cursor()
    sql = "SELECT * FROM addquestions WHERE uid = %s"
    cursor.execute(sql, (uid,))
    
    # Fetch all rows from the query result
    rows = cursor.fetchall()
    
    # Initialize counts
    yes_count = 0
    no_count = 0
    
    # Iterate through each row
    for row in rows:
        # Iterate through each answer column
        for answer in row[1:]:  # Assuming the first column is not an answer
            # Convert answer to string to handle potential integers
            answer_str = str(answer)
            # Check if the answer is 'yes' or 'no' and update counts accordingly
            if answer_str.lower() == 'yes':
                yes_count += 1
            elif answer_str.lower() == 'no':
                no_count += 1
    
    # Print the counts for debugging
    print("Count of 'yes':", yes_count)
    print("Count of 'no':", no_count)
    
    # Determine the message based on counts
    if yes_count > no_count:
        # message = "Your child needs a consultation with a doctor."
        return render(request,'doctorconsult.html')
    elif yes_count < no_count:
        # message = "Doctor consultation is not needed at the moment."
        return render(request,'counsellorconsult.html')
    else:
        # message = "Your child's situation is inconclusive. Please consult a doctor for further evaluation."
        message = "Your child's situation is normal. Please take your child."
        return HttpResponse(message)
        
    


def doctorconsult(request):
     return render(request,'doctorconsult.html')
def counsellorconsult(request):
     return render(request,'counsellorconsult.html')

    
   


def uViewDoctor(request):
    cursor=connection.cursor()
    s6="select * from doctor inner join login on doctor.doctorid=login.uid where login.type='Doctor' and login.status='approved'"
    cursor.execute(s6)
    doctorviewresult=cursor.fetchall()
    doctorlist=[]
    for row in doctorviewresult:
        q={'doctorid':row[0],'name':row[1],'dob':row[2],'sex':row[3],'address':row[4],'city':row[5],'pincode':row[6],'qualification':row[8],'exp':row[9],'phno':row[10],'email':row[11],'type':row[12],'uid':row[13],'username':row[14],'password':row[15],'type':row[16],'status':row[17]}
        doctorlist.append(q)
    return render(request,'uViewDoctor.html',{'doctorlist':doctorlist})

def book(request):
    cursor = connection.cursor()
    did = request.GET['id']
    uid = request.session['uid']
    today = date.today()
    status = 'pending'  # Assuming 'status' should always be 'pending' here
    
    # Use parameterized query to avoid SQL injection
    sql = "INSERT INTO book (uid, did, bdate,udate,status) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (uid, did, today, status))
    
    msg = "<script>alert('Added Successfully');window.location='/uViewDoctor/'</script>"
    return HttpResponse(msg)

def Ubookstatus(request):
    cursor=connection.cursor()
    uid = request.session['uid']
    # s= "SELECT * FROM book INNER JOIN doctor ON book.did = doctor.doctorid inner join time on book.bid=time.bid WHERE book.uid = '%s'"%(uid)
    # print(s)
    # cursor.execute(s)
    # result=cursor.fetchall()
    # cursor=[]
    # for row in result:										
    #     q={'bid':row[0],'uid':row[1],'did':row[2],'bdate':row[3],'udate':row[4],'status':row[5],'doctorid':row[6],'name':row[7],'dob':row[8],'sex':row[9],'address':row[10],'city':row[11],'pincode':row[12],'qualification':row[13],'exp':row[14],'phno':row[15],'email':row[16],'type':row[17],'tuid':row[18],'uid':row[19],'bid':row[20],'utime':row[21]}
    #     cursor.append(q)
    s3="SELECT * FROM book INNER JOIN doctor ON book.did = doctor.doctorid WHERE book.uid = '%s'"%(uid)   
    print(s3)
    cursor.execute(s3)
    result=cursor.fetchall()
    cursor=[]
    for row in result:										
        q3={'bid':row[0],'uid':row[1],'did':row[2],'bdate':row[3],'udate':row[4],'status':row[5],'doctorid':row[6],'name':row[7],'dob':row[8],'sex':row[9],'address':row[10],'city':row[11],'pincode':row[12],'qualification':row[13],'exp':row[14],'phno':row[15],'email':row[16],'type':row[17]}
        cursor.append(q3) 
    return render(request,'Ubookstatus.html',{'cursor':cursor})

def utime(request):
    cursor=connection.cursor()
    uid = request.session['uid']
    s3="SELECT * FROM time WHERE time.uid = '%s'"%(uid)   
    print(s3)
    cursor.execute(s3)
    result=cursor.fetchall()
    cursor=[]
    for row in result:										
        q3={'tuid':row[0],'uid':row[1],'bid':row[2],'utime':row[3]}
        cursor.append(q3) 
    return render(request,'utime.html',{'cursor':cursor})



def doctorviewbook(request):
    cursor=connection.cursor()
    uid = request.session['uid']
    s= "SELECT * FROM book INNER JOIN ureg ON book.uid = ureg.userid WHERE book.did = '%s'"%(uid)
    print(s)
    cursor.execute(s)
    result=cursor.fetchall()
    cursor=[]
    for row in result:
        q={'bid':row[0],'uid':row[1],'did':row[2],'bdate':row[3],'udate':row[4],'status':row[5],'userid':row[6],'childname':row[7],'dob':row[8],'sex':row[9],'parentname':row[10],'address':row[11],'city':row[12],'pincode':row[13],'phn':row[14],'email':row[15]}
        cursor.append(q)
        bid=row[0]
        print(bid)
        userid=row[5]
    return render(request,'doctorviewbook.html',{'cursor':cursor,'userid':userid,'bid':bid})

def baccept(request):
    cur=connection.cursor()
    id=request.GET['id']
    sql="update book set status='approved' where bid='%s'"%(id)
    cur.execute(sql)
    msg="<script>alert('Status updated');window.location='/doctorviewbook/'</script>"
    return HttpResponse(msg)
def breject(request):
    cur=connection.cursor()
    id=request.GET['rid']
    sql="update book set status='rejected' where bid='%s'"%(id)
    cur.execute(sql)
    msg="<script>alert('Status updated');window.location='/doctorviewbook/'</script>"
    return HttpResponse(msg)

def feedback(request):
     return render(request,'feedback.html')

def feedaction(request):
    cursor = connection.cursor()
    did = request.GET['feed']
    uid=request.session['uid']
    # Use parameterized query to avoid SQL injection
    sql = "INSERT INTO feedback (uid, feedback) VALUES (%s, %s)"
    cursor.execute(sql, (uid, did))
    
    msg = "<script>alert('Added Successfully');window.location='/feedback/'</script>"
    return HttpResponse(msg)

def taction(request):
    cursor = connection.cursor()
    bid = request.GET['bid']
    uid = request.GET['uid']
    did = request.GET['t']
  
    # Use parameterized query to avoid SQL injection
    sql = "INSERT INTO time (uid,bid, utime) VALUES (%s, %s,%s)"
    cursor.execute(sql, (uid,bid, did))
    
    msg = "<script>alert('Added Successfully');window.location='/doctorviewbook/'</script>"
    return HttpResponse(msg)

def bookD(request):
    cursor=connection.cursor()
    id=request.GET['id']
    uid=request.session['uid']
    s="select * from ureg where userid='%s'"%(uid)
    cursor.execute(s)
    userviewresult=cursor.fetchall()
    userlist=[]
    for row in userviewresult:
        q={'userid':row[0],'childname':row[1],'dob':row[2],'sex':row[3],'parentname':row[4],'address':row[5],'city':row[6],'pincode':row[7],'phn':row[8],'email':row[9]}
        userlist.append(q)
    return render(request,'bookc.html',{'userlist':userlist,'id':id})

def uViewCounsellor(request):
    cursor=connection.cursor()
    s6="select * from doctor inner join login on doctor.doctorid=login.uid where login.type='Counsellor' and login.status='approved'"
    cursor.execute(s6)
    doctorviewresult=cursor.fetchall()
    doctorlist=[]
    for row in doctorviewresult:
        q={'doctorid':row[0],'name':row[1],'dob':row[2],'sex':row[3],'address':row[4],'city':row[5],'pincode':row[6],'qualification':row[8],'exp':row[9],'phno':row[10],'email':row[11],'type':row[12],'uid':row[13],'username':row[14],'password':row[15],'type':row[16],'status':row[17]}
        doctorlist.append(q)
    return render(request,'uViewCounsellor.html',{'doctorlist':doctorlist})

def bookc(request):
    cursor=connection.cursor()
    id=request.GET['id']
    uid=request.session['uid']
    s="select * from ureg where userid='%s'"%(uid)
    cursor.execute(s)
    userviewresult=cursor.fetchall()
    userlist=[]
    for row in userviewresult:
        q={'userid':row[0],'childname':row[1],'dob':row[2],'sex':row[3],'parentname':row[4],'address':row[5],'city':row[6],'pincode':row[7],'phn':row[8],'email':row[9]}
        userlist.append(q)
    return render(request,'bookc.html',{'userlist':userlist,'id':id})

def bookcaction(request):
    cursor = connection.cursor()
    cid = request.GET['id']
    uid=request.session['uid']
    udate = request.GET['udate']
    today = date.today()
  
    # Use parameterized query to avoid SQL injection
    sql = "INSERT INTO book (uid,did,bdate,udate,status) VALUES (%s, %s,%s,%s,%s)"
    cursor.execute(sql, (uid,cid,today, udate,'pending'))
    
    msg = "<script>alert('Added Successfully');window.location='/uViewCounsellor/'</script>"
    return HttpResponse(msg)

def counsellorhome(request):
    return render(request,'counsellorhome.html')

def viewfeedback(request):
    cursor=connection.cursor()
    s="select * from feedback inner join ureg on feedback.uid=ureg.userid"
    cursor.execute(s)
    userviewresult=cursor.fetchall()
    userlist=[]
    for row in userviewresult:
        q={'fid':row[0],'uid':row[1],'feedback':row[2],'parentname':row[7]}
        userlist.append(q)
    return render(request,'viewfeedback.html',{'userlist':userlist})

def reports(request):
    cur = connection.cursor()
    cr = []
    sql = None  # Initialize sql outside the if statement

    if request.method == 'GET' and 'd1' in request.GET and 'd2' in request.GET:
        d1 = request.GET['d1']
        d2 = request.GET['d2']
        # sql = "SELECT * FROM book WHERE udate BETWEEN '%s' AND '%s'" % (d1, d2)
        sql="SELECT * FROM book INNER JOIN ureg ON book.uid = ureg.userid INNER JOIN doctor ON doctor.doctorid = book.did WHERE udate BETWEEN '%s' AND '%s'" % (d1, d2)
        

    if sql:
        cur.execute(sql)
        rs = cur.fetchall()

        for row in rs:
            q = {'bid':row[0],'uid':row[1],'did':row[2],'bdate':row[3],'udate':row[4],'status':row[5],'userid':row[6],'childname':row[7],'dob':row[8],'sex':row[9],'parentname':row[10],'address':row[11],'city':row[12],'pincode':row[13],'phn':row[14],'email':row[15],'doctorid':row[16],'name':row[17],'dob':row[18],'sex':row[19],'address':row[20],'city':row[21],'pincode':row[22],'qualification':row[23],'exp':row[24],'phno':row[25],'email':row[26],'type':row[27]}
            cr.append(q)

    return render(request, 'reports.html', {'cr': cr})