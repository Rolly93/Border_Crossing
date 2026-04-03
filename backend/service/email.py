import os
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig

class Emailservice(object):
    """docstring for Emailservice."""
    def __init__(self,username,password,domain):
        
