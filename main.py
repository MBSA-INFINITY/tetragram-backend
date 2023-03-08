from flask import Flask,render_template,request
from firebase import Firebase
import os
import random,string
try:
    os.mkdir("blog")
except:
    pass
app = Flask(__name__)
firebaseConfig = {
 "apiKey": "AIzaSyA1jInhoZF7JyTK9gIo_zx6z43YmIOoL1o",
  "authDomain": "py-ssg.firebaseapp.com",
  "projectId": "py-ssg",
  "storageBucket": "py-ssg.appspot.com",
  "messagingSenderId": "565484331912",
  "appId": "1:565484331912:web:3ffab59d23fd071bfed03d",
  "measurementId": "G-EYJGFCNC51",
  "databaseURL":"https://py-ssg-default-rtdb.firebaseio.com"
}
firebase = Firebase(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

def random_string(N):
  res = ''.join(random.choices(string.ascii_uppercase +
                              string.digits, k=N))
  return str(res)

@app.route("/",methods = ['GET','POST'])
def start():
    if request.method == 'POST':
        foldername = random_string(10)
        slug = request.form.get("slug")
        markdown = request.form.get("markdown")
        data = {
            "slug":slug,
            "foldername":foldername
        }
        db.child("blogs").push(data)
        with open(f"local_files/content.md" ,'w') as file:
          file.write(markdown)
        storage.child(f"{foldername}/content.md").put("local_files/content.md")
        os.remove("local_files/content.md")
        return render_template("index.html")
    return render_template("index.html")


if  __name__ == "__main__":
    app.run(debug = True)