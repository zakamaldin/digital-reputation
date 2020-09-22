# DIGITAL-REPUTATION Test for BackEnd Python Developer
This application is created for testing people by test.

Administrator can add new tests, questions for tests and answers for questions.

This application provide functional for registration people and approving their accounts by email.

## Instruction
pip install -r requirements.txt  
python manage.py migrate  
python manage.py createsuperuser  
python manage.py runserver 8000  
#### If you want to enable auth system for registrating people
#### You need to use debug SMTP server by nex command (in additional terminal):
python -m smtpd -n -c DebuggingServer localhost:7777
#### Or set credentials of your Prod SMTP server in Env. variables
please check digital_reputation_test/settings.py to set right Env. variables in your OS

