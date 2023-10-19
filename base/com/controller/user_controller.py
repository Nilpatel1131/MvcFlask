from base import app
from flask import render_template, request, flash, redirect
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.user_dao import UserDAO
import random
import string
import bcrypt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base.com.controller.login_controller import login_required


@app.route('/user/load_user')
def admin_load_user():
    return render_template("user/adduser.html")


@app.route('/user/insert_user', methods=['post'])
def user_insert_user():
    try:
        login_vo = LoginVO()
        login_dao = LoginDAO()

        user_vo = UserVO()
        user_dao = UserDAO()
        login_username = request.form.get('loginUsername')
        user_firstname = request.form.get('userFirstname')
        user_lastname = request.form.get('userLastname')
        user_address = request.form.get('userAddress')
        user_gender = request.form.get('userGender')
        login_vo_list = login_dao.view_login()
        print("login_vo_list >>>>>>", login_vo_list)
        login_username_list = [i.as_dict()['login_username'] for i in login_vo_list]
        print("login_username_list >>>>>", login_username_list)
        if login_username in login_username_list:
            error_message = "The username already exists !"
            flash(error_message)
            return redirect('/')
        login_password = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
        salt = bcrypt.gensalt(rounds=12)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>", login_password)
        hashed_login_password = bcrypt.hashpw(login_password.encode("utf-8"), salt)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", hashed_login_password)

        sender = "nilpatel.1532@gmail.com"
        password = "myvittauqanqocth"
        receiver = login_username

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "YOUR SYSTEM GENERATED LOGIN PASSWORD IS:"
        msg.attach(MIMEText(login_password, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()

        login_vo.login_username = login_username
        login_vo.login_password = hashed_login_password
        login_vo.login_role = "user"
        login_vo.login_status = True
        login_dao.insert_login(login_vo)

        user_vo.user_firstname = user_firstname
        user_vo.user_lastname = user_lastname
        user_vo.user_gender = user_gender
        user_vo.user_address = user_address
        user_vo.user_login_id = login_vo.login_id
        user_dao.insert_user(user_vo)
        return redirect("/")
    except Exception as ex:
        print("user_insert_user route exception occured>>>>>>>>>>", ex)
        return render_template('user/viewError.html', ex=ex)



@app.route('/admin/view_user')
@login_required('admin')
def admin_view_user():
    try:
        user_dao = UserDAO()
        user_vo_list = user_dao.view_user()
        return render_template('admin/viewUser.html',
                               user_vo_list=user_vo_list)
    except Exception as ex:
        print("admin_view_user route exception occurred>>>>>>>>>>", ex)
        return render_template('admin/viewError.html', ex=ex)
