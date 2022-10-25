from flask import  session
import smtplib

class MailService:
    """
        This class handles, sending of mails to the user on various occations.
        Ex. OTP, Update on Leave etc.
    """
    def __init__(self) -> None:
        self.OriginalOTP = -1

    def send_otp(self,email,otp):
        """
            Function to send the OTP to the user, for email verification.
        """
        session['otp'] = otp
        message = "Your OTP for IIT Ropar Leave Management Portal is " + str(otp)
        subject = "OTP - IIT Ropar Leave Management Portal"
        
        self.send_mail(email,message,subject)

    def send_mail(self,receiver , message , subject = ""):
        """
            Generic mail sending function, takes message, mail subject and receiver as input.
        """
        final_message = "Subject: {}\n\n{}".format(subject,message)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("leavemanagementiitropar@gmail.com", "gdpzrofppayyvscw")

        server.sendmail("leavemanagementiitropar@gmail.com",receiver,final_message)
        server.quit()

MS = MailService()