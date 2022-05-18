# Leave-Portal


## Submitted By
Group X8

Members:<br>
Apurv Rathore         2019CSB1077<br>
Sangram Jagadale   2019CSB1091<br>
Jaglike Makkar         2019CSB1092<br>

## Submitted To
Dr. Puneet Goyal <br>
(Department of Computer Science and Engineering, IIT Ropar)<br>



## Description of our App
To apply for a leave, faculty and staff members have to go through a lot of paperwork. Our task is to design the Leave Management Portal that will digitalize the leave management system at IIT Ropar. 
The faculties and staff members can fill the leave application form online and view/download the leaves they have applied. The HoDs and Dean can view the respective leave applications and can Approve/Disapprove them or add any comment.



## Technologies/Tools used

Frontend: React<br>
Backend: Flask<br>
Database: MySql, Google drive<br>
Deployment: Heroku (Backend), Vercel (Frontend)<br>




## How to run the App

To install the required modules and libraries
> pip install requirements.txt 


To run the frontend
> cd frontend

> npm install

> npm start


To run the server
> cd server

> python app.py

## Directory Structure

+---frontend
|   |   package-lock.json
|   |   package.json
|   |        
|   \---src
|       |   App.js
|       |   App.test.js
|       |   httpClient.js
|       |   index.js
|       |   logo.svg
|       |   
|       +---components
|       |   |   CheckLeaves.js
|       |   |   Dashboard.js
|       |   |   DeanDashboard.js
|       |   |   DisplayLeaves.js
|       |   |   FacultyDashboard.js
|       |   |   Footer.js
|       |   |   Intro.js
|       |   |   LeaveForm.js
|       |   |   LoginForm.js
|       |   |   Navbar.js
|       |   |   OtpVerification.js
|       |   |   Table.js
|       |   |   
|       |   \---helpers
|       |           validators.js
|       |           
|       +---css
|       |       App.css
|       |       CheckLeaves.css
|       |       Dashboard.css
|       |       DisplayLeaves.css
|       |       index.css
|       |       LeaveForm.css
|       |       Login.css
|       |       Table.css
|       |       
|       \---imgs
|               background.jpg
|               background2.webp
|               loginIcon.png
|               
\---server
        app.py
        client_secrets.json
        
