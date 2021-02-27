# flask-blog
A simple blog written using python Flask.
Deployed on Heroku (https://nurlybek-simple-blog.herokuapp.com/)

# Install guide
Clone it with
```
git clone https://github.com/nurlybek-dev/flask-blog.git
cd flask-blog
pip install -r requirements.txt
set FLASK_APP=main.py
flask create-db
flask run
```
Open http://127.0.0.1:5000/ in your browser.


To create super user use command
```
flask createsuperuser --username <name> --password <password>
```
