from flask import Flask, render_template, request, redirect
from firebase import Firebase
import os, json, random, string, tempfile, requests

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
    "databaseURL": "https://py-ssg-default-rtdb.firebaseio.com"
}
firebase = Firebase(firebaseConfig)
db = firebase.database()
storage = firebase.storage()


def random_string(N):
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    return str(res)

# @app.route("/",methods = ['GET','POST'])
# def start():
#     if request.method == 'POST':
#         foldername = random_string(10)
#         slug = request.form.get("slug")
#         markdown = request.form.get("markdown")
#         data = {
#             "slug":slug,
#             "foldername":foldername
#         }
#         db.child("blogs").push(data)
#         with open(f"local_files/content.md" ,'w') as file:
#           file.write(markdown)
#         storage.child(f"{foldername}/content.md").put("local_files/content.md")
#         os.remove("local_files/content.md")
#         return render_template("index.html")
#     return render_template("index.html")

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/get_blogs", methods=['GET'])
def blogs_to_json():
    blogs = db.child("blogs").get()
    blogs = blogs.val()
    blog_array = []
    for doc_id, blog in blogs.items():
        markdown_url = storage.child(f"{blog['foldername']}/content.md").get_url(None)
        image_url = storage.child(f"{blog['foldername']}/thumbnail.jpg").get_url(None)
        print(markdown_url)
        response = requests.get(markdown_url)
        with open("file.txt", "wb") as f:
            f.write(response.content)
        with open("file.txt", "r") as f:
            file_contents = f.read()
        print(image_url)
        blog_to_append = {
            'title': blog["title"],
            'author': blog["author"],
            'description': blog["description"],
            'slug': blog["slug"],
            'image_url': image_url,
            'markdown': file_contents
        }
        blog_array.append(blog_to_append)
        os.remove("file.txt")
    with open("data.json", "w") as f:
        f.write(json.dumps({'blogs': blog_array}))
    return json.dumps({'blogs': blog_array}), 200


@app.route("/blog", methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        foldername = random_string(10)
        slug = request.form.get("slug")
        markdown = request.form.get("markdown")
        title = request.form.get("title")
        author = request.form.get("author")
        description = request.form.get("description")
        thumbnail = request.files.get("thumbnail")
        data = {
            "slug": slug,
            "foldername": foldername,
            "title": title,
            "author": author,
            "description": description
        }
        db.child("blogs").push(data)
        with open(f"local_files/content.md", 'w') as file:
            file.write(markdown)
        temp = tempfile.NamedTemporaryFile(delete=False)
        thumbnail.save(temp.name)
        storage.child(f"{foldername}/content.md").put("local_files/content.md")
        storage.child(f"{foldername}/thumbnail.jpg").put(thumbnail)
        os.remove("local_files/content.md")
        temp.close()
        os.remove(temp.name)
    return render_template("blog.html")


if __name__ == "__main__":
    app.run(debug=True)
