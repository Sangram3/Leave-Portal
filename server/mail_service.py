from flask import  session
import smtplib

class MailService:

    def __init__(self) -> None:
        self.OriginalOTP = -1

    def send_otp(self,email,otp):
        session['otp'] = otp
        msg = "Your OTP for IIT Ropar Leave Management Portal is " + str(otp)
        self.send_mail(email,msg,"OTP - IIT Ropar Leave Management Portal")

    def send_mail(self,receiver , message , subject = ""):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("leavemanagementiitropar@gmail.com", "gdpzrofppayyvscw")
        server.sendmail(subject,receiver,message)

        