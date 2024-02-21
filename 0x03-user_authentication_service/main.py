#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
email2 = 'bob@boob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)
auth.register_user(email2, password)

print(auth.create_session(email))
print(auth.create_session(email2))
print(auth.create_session("unknown@email.com"))