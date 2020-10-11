![dash-flask-login](https://user-images.githubusercontent.com/31367475/47422577-4f761500-d759-11e8-90c2-b70a79fcd610.gif)

username: `test`
pwd: `test1`
You can add more users using the 
`add_remove_users.ipynb` jupyter notebook
 or
by the functional of`users_mgt.py`

### Files description:
`add_remove_users.ipynb`: A jupyter notebook to help creating and removing users<br/>
`app.py`: The app initial screen<br/>
`config.py`: python script to initialize the configuration included in the `config.txt` file<br/>
`config.txt`: configuration file<br/>
`server.py`: the app initialization file<br/>
`users.db`: sqlite3 database with user information<br/>
`users_mgt.py`: helper file for the user management process<br/>

### Running an app locally

To run an app locally:

1. (optional) create and activate new virtualenv:
	virtualenv venv
```#(optional):
	swithch to python3.8:
	sudo update-alternatives --config python3
	source venv/bin/activate
```

2. `pip install -r ./Install/Result.txt`
3. `bash start.sh`
4. open http://127.0.0.1:5000 in your browser or
5. `flask run --host=0.0.0.0` or `gunicorn --bind 0.0.0.0:8000 wsgi:application` to open for external connections

### Deployng to Heroku
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login to your heroku account: `heroku login`
3. Create the app: `heroku create`
4. Deploy to Heroku: `git push heroku master`
5. Access the app via the address provided by Heroku
