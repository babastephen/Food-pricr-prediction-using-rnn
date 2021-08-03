from datetime import datetime as dt, datetime
import pandas as pd
import mysql.connector as conn
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
vals = ''
data = []
location = ''

mydb = conn.connect(
    host='localhost',
    user='root',
    password='1234',
    database='price_prediction'
)

mycursor = mydb.cursor()
    # NB : you won't get an IntegrityError when reading




# Create your views here.
def getlocation(request):
    global data
    global location
    if 'location' in request.POST:
        location = request.POST['location']
        data = pd.read_csv(f"D:/Programing/FinalYear/Price_Prediction/maize_white/{location}")
        return redirect(predict)
    return render(request, 'location.html')


def userSignUp(request):
    if request.method == 'POST':
        Username = request.POST['username']
        UserPassword = request.POST['password']
        ConfrimPassword = request.POST['cpassword']
        PhoneNumber = request.POST['phone']
        DateOfRegistration = datetime.now()
        mycursor.execute("SELECT * from customer WHERE Username =%s or  PhoneNumber = %s", (Username, PhoneNumber,))
        if len(mycursor.fetchall()) > 0:
            messages.success(request, 'username or phonenumber already exist')
        else:
            if UserPassword != ConfrimPassword:
                messages.warning(request, "Password and confirmpassword are not the same")
            elif len(UserPassword) < 8 or len(ConfrimPassword) < 8:
                messages.warning(request, "Password and confirmpassword length must be 8 or more")
            else:
                sql = 'insert into customer(Username, UserPassword, PhoneNumber,DateOfRegistration)values(%s,%s,%s,%s)'
                val = (Username, UserPassword, PhoneNumber, DateOfRegistration)
                mycursor.execute(sql, val)
                mydb.commit()
                messages.info(request, 'Successfully signed up')
    return render(request, 'UserSignUp.html')


user = ''
password = ''

def login(request):
    global user, password
    if request.method == 'POST':
        user = request.POST['user']
        password = request.POST['password']
        mycursor.execute("SELECT * from customer WHERE Username =%s AND  UserPassword = %s", (user, password,))
        if len(mycursor.fetchall()) > 0:
            return redirect(getlocation)
        else:
            messages.warning(request, 'username or password incorrect!')
    return render(request, 'UserLogin.html')
def ResetPassword(request):
    if request.method == 'POST':
        phonenumber = request.POST['phone']
        newpassword = request.POST['password']
        if len(newpassword)<8:
            messages.success(request, "Password length should be 8 or more characters")
        else:
           mycursor.execute("SELECT * from customer WHERE PhoneNumber =%s" , (phonenumber,))
           if len(mycursor.fetchall()) > 0:
                mycursor.execute("update customer set UserPassword = %s WHERE PhoneNumber = %s",(newpassword,phonenumber))
                mydb.commit()
                return redirect(login)
           else:
                messages.success(request, "phone number does not exist, please re-enter phone number")
    return render(request, 'PasswordReset.html')
#
def regression(request):
    return render(request, 'RegressionAnalysis.html')
def home(request):
    return render(request, 'home.html')


#
#
val = 0
my = []
vals = ''
val_p=0
error=0

def predict(request):
    global val,vals,data,val_p,error
    # data = pd.read_csv(f"D:/Programing/FinalYear/Price_Prediction/maize_white/{user}")
    my = data['Date']
    if 'predict_date' in request.POST:
        vals = request.POST['predict_date']
        val = data.loc[data['Date'] == vals]
        val_p = val['Maize_White']
        error = val['perform']
        val_p = round(float(val_p),2)
        error = round(float(error),2)
       # val_p = round(float(error + val_p), 2)
    return render(request, 'Predict.html', {'name': location, 'price': val_p, 'dat': my, 'day': vals,'error':error})
