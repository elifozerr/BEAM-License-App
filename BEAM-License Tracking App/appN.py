#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 18:40:37 2020

@author: elifozer
"""


from flask import Flask, render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
import random



class RegisterForm(Form):
    company = StringField("Şirket Adı:", validators=[validators.DataRequired()])
    person = StringField("Yetkili Kişi:")
    position = StringField("Yetkilinin Görevi:")
    tel = StringField("Yetkilinin İletişim Bilgisi:")
    model= StringField("Model:  Cloud veya On-premise")
    type=StringField("Type:") #type field
    time=StringField("Lisansın Bitme Tarihi:")
    counter=StringField("Kullanıcı Sayısı:")
    #id=StringField("ID:", validators = [validators.DataRequired(message="Butona tıklayarak ID oluşturun...")])
    
    
#create app object
app = Flask(__name__)

app.secret_key= "beaml"

#configuration
app.config["MYSQL_HOST"] = "localhost" 
app.config["MYSQL_USER"] = "root" 
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "license"

#curser class - dictionary curser
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

#function for creating id
def create_id():
    
    num1 = random.randint(10000, 99999)
    #print("Random integer: ",num1)
    num2 = random.randint(1000, 9999)
    converted_num1 = str(num1)
    converted_num2 = str(num2)
    converted = converted_num1 + converted_num2
    print("ID: ",converted)
    return converted
    
   
create_id()


#request for http respond
#MAIN
@app.route("/")
def index2():
  
    cursor = mysql.connection.cursor()
    sorgu = "Select * From beaml"
    result = cursor.execute(sorgu)
        
    if result > 0:
        beaml = cursor.fetchall()
        return render_template("index2.html",beaml = beaml)
    else:   
        return render_template("index2.html") #returns html code as response



#request for htt response -HELP PAGE
@app.route("/help")
#function for url adress
def help():
    return render_template("helpfile.html") #returns html code as response


#CREATE LICENSE PAGE
#function can take 2 requests 
@app.route("/create",methods = ["GET", "POST"])
#function for url adress
def create():
    
    form = RegisterForm(request.form) 
    
    if request.method == "POST" and form.validate():
        
        company = form.company.data
        person = form.person.data
        position = form.position.data
        tel= form.tel.data
        model = form.model.data
        type = form.type.data
        time = form.time.data
        counter = form.counter.data
        id = create_id()
        #id = form.id.data
        
        
        if model == "Cloud" :
            
            id = "CLD" + id
        
        elif model == "On-premise" :
            
            id = "ONP" + id
            
        
        else:
            
  
            flash("Lütfen geçerli bir model giriniz","danger")
            return redirect(url_for("index2"))
            
            
            
        
        cursor = mysql.connection.cursor()
        
        sorgu = "Insert into beaml(company,person,position,tel,model,type,time,counter,id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(sorgu,(company,person,position,tel,model,type,time,counter,id)) 
        mysql.connection.commit()
        #
        cursor.close()
        
       
        flash("Lisans Başarıyla Oluşturuldu...","success")
        
    
        return redirect(url_for("index2"))
    else:
       
        return render_template("license.html", form =form) #returns html code as response

#delete page
@app.route("/delete/<string:id>")
def delete(id):
    
    cursor = mysql.connection.cursor()
    
    sorgu ="Select * from beaml"
    result = cursor.execute(sorgu)
    
    if result > 0:
        sorgu2 = "Delete from beaml where id = %s"
        cursor.execute(sorgu2,(id,))
        
        mysql.connection.commit()
        flash("Lisans silindi","success")
        return redirect(url_for("index2"))
        
    else:
        flash("Lisans silinemedi","danger")

#Update page
@app.route("/edit/<string:id>", methods = ["GET","POST"])
def update(id):
    
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        
        sorgu = "Select * from beaml where id = %s"
        result = cursor.execute(sorgu,(id,))
        
        if result == 0:
            flash("Lisans güncellenmedi","danger")
            return redirect(url_for("index2"))
        else:
            license = cursor.fetchone()
            form = LicenseForm()
            
            form.company.data = license["company"]
            form.person.data = license["person"]
            form.position.data = license["position"]
            form.tel.data = license["tel"]
            form.model.data = license["model"]
            form.type.data = license["type"]
            form.time.data = license["time"]
            form.counter.data = license["counter"]
            form.id.data = license["id"]
            
            return render_template("update.html",form = form)
    #post request     
    else:
        form = LicenseForm(request.form)
        
        newCompany = form.company.data
        newPerson = form.person.data
        newPosition = form.position.data
        newTel = form.tel.data
        newModel= form.model.data
        newType = form.type.data
        newTime = form.time.data
        newCounter = form.counter.data
        newID = form.id.data
        
        sorgu2 ="Update beaml Set company = %s, person = %s, position = %s, tel = %s, model = %s, type = %s, time = %s, counter = %s, id = %s where id = %s"
        
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu2,(newCompany,newPerson,newPosition,newTel,newModel,newType,newTime,newCounter,newID,id))
        
        mysql.connection.commit()
        
        flash("Lisans Başarıyla Güncellendi","success")
        
        return redirect(url_for("index2"))
        
#request for http response -found license page
@app.route("/found")
#function for url address
def find():
    
    cursor = mysql.connection.cursor()
    
    sorgu = "Select * From beaml"
    result = cursor.execute(sorgu)
        
    if result > 0:
        beaml = cursor.fetchall()
        return render_template("index2.html",beaml = beaml)
    else:   
        
        return render_template("index2.html") #returns html code as response
    
    
    return render_template("found.html") #returns html code as response

#Details of person
@app.route("/details/<string:id>")
#function for url adress
def detail(id):
    
    cursor = mysql.connection.cursor()
    
    sorgu = "Select * from beaml where id = %s"
    result = cursor.execute(sorgu,(id,))
    
    if result > 0:
        beaml = cursor.fetchone()
        return render_template("details.html",beaml = beaml)
    else:   
        
        return render_template("details.html") #returns html code as response
    


#Lisans Form
class LicenseForm(Form):
    
    company = StringField("Şirket")
    person = StringField("Yetkili Kişi:")
    position = StringField("Yetkilinin Görevi:")
    tel = StringField("Yetkilinin İletişim Bilgisi:")
    model= StringField("Model: Cloud veya On-premise")
    type=StringField("Type:") #type field
    time=StringField("Lisansın Bitme Tarihi:")
    counter=StringField("Kullanıcı Sayısı:")
    id=StringField("ID:")

#Search url
@app.route("/search", methods = ["GET","POST"])
def search():
    
    if request.method == "GET":
        
        return redirect(url_for("index2"))
    
    else:
        
        keyword = request.form.get("keyword")
        
        cursor = mysql.connection.cursor()
        
        sorgu = "Select * from beaml where company like '%" + keyword  + "%' "
        
        result = cursor.execute(sorgu)
        
        if result == 0:
            
            flash("Aranan kelimeye uygun şirket bulunamadı","warning")
            return redirect(url_for("find"))

        else:
            
            beaml = cursor.fetchall()
            
            return render_template("found.html", beaml = beaml)
    


if __name__ == "__main__":
    app.run(debug=True)
    
    



