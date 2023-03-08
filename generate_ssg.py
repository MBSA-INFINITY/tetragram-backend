from firebase import Firebase
import os
try:
    os.mkdir("blog")
except:
    pass
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
all_blogs = db.child("blogs").get().val()
all_blogs_html_str = ""
for key,blog in all_blogs.items():
    slug = blog['slug']
    foldername = blog['foldername']
    all_blogs_html_str+=f"<a href='/blog/{slug}' target='_blank'>{slug}</a><br>"
    try:
        os.mkdir(f"blog/{slug}")
        os.mkdir(f"blog/{slug}/docs")
        with open(f"blog/{slug}/index.html" ,'w') as file:
            content = """
            <html lang="en-us">

        <head>
        <script type="module" src="https://cdn.jsdelivr.net/gh/zerodevx/zero-md@2/dist/zero-md.min.js"></script>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
        </head>

        <body>
        <nav class="navbar navbar-expand-lg bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">Home</a>
                </li>
                <li class="nav-item">
                <a class="nav-link" href="#">Link</a>
                </li>
                <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Dropdown
                </a>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#">Action</a></li>
                    <li><a class="dropdown-item" href="#">Another action</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="#">Something else here</a></li>
                </ul>
                </li>
                <li class="nav-item">
                <a class="nav-link disabled">Disabled</a>
                </li>
            </ul>
            <form class="d-flex" role="search">
                <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
            </div>
        </div>
        </nav>
        <div style="width:70%; margin:0 auto;" id="mdcontainer">
        <zero-md src="./docs/content.md" no-shadow="">

        </zero-md>
        </div>
        </body>

        <script>
        function getQuery(key) {
        var query = window.location.search.substring(1);
        var key_values = query.split("&");
        var params = {};
        key_values.map(function (key_val) {
            var key_val_arr = key_val.split("=");
            params[key_val_arr[0]] = key_val_arr[1];
        });
        if (typeof params[key] != "undefined") {
            return params[key];
        }
        return "";
        }

        window.onload = function () {
        md = document.createElement("zero-md")
        md.setAttribute("src", "./docs/mbsa.md")
        // md.setAttribute("src", getQuery("src"))
        md.setAttribute("no-shadow", "")
        document.getElementById("mdcontainer").append(md)
        }
        </script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>

        </html>"""
            file.write(content)
        storage.child(f"{foldername}/content.md").download(f"blog/{slug}/docs/content.md")
    except:
        pass
    with open("index.html",'w') as f:
        f.write("<html><head></head><body>")
        f.write(all_blogs_html_str)
        f.write("</body>")