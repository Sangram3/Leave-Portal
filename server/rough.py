# credentials = open("C:\\Academics\\6th Sem\\CP301_DP\\oAuthCredentials.txt").readlines()
# my_client_id = credentials[0].strip()
# my_secret = credentials[1].strip()

# google = oauth.register(
#     name='google',
#     client_id=my_client_id,
#     client_secret=my_secret,
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
#     client_kwargs={'scope': 'openid email profile'},
# )

    
# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         connect = db.connect()
#         cursor = connect.cursor()
#         cursor.execute("SELECT * FROM user_auth WHERE username = %s",(username))
#         data = cursor.fetchall()
#         if not data:
#             cursor.execute("INSERT INTO user_auth(username, password) VALUES (%s, %s)",(username, password))
#             connect.commit()
#             cursor.close()
#             session["logged_in"]=1
#             session["username"]=username
#             return render_template('home.html')
#         else:
#             return "Username already exists."
#     return render_template('register.html')
