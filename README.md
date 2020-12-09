# MDC Online Class Attender :robot:
> Miami Dade Collage Class Attender

This bot can automatically join online classes that are held in [MDC BlackBoard Collaborate](https://mdc.blackboard.com/). The bot will join the class according to the given schedule. You could use this bot if your professors put the link of the classes in BlackBoard. If you have to join the classes by a link sent from the professor you could use this project as a guide and create your bot. 

## Setup :gear:
There is a couple of things you need to setup before running the bot:
1. Open bot.py, and put your MDC credentials in the CREDS dictionary.
* Example - ```CREDS = {'email' : 'myemail@gmail.com', 'passwd': 'mypassword'}```
2. In the same file you will have to change or add the names of how your professor calls the virtual room link.
* Example - ```common_names = ['VIRTUAL ROOM', 'BB Coll Ultra']```
3. Make sure that the timezone of the computer is correct.

## Installation :arrow_down:
* Clone the repository locally ```git clone https://github.com/javier-arango/class-attender-bot```
* Install requirements.txt ```pip install -r requirements.txt```

## Technologies :computer:
Project is created with:
* Python version: 3.7.5
* Selenium version: 3.141.0
* Schedule version: 0.6.0
* Google Chrome version: 87.0.4280.88

## Note :pencil:
**This project is for educational purposes only - I will no be responsible for any issues related to your attendance or anything about your class**.
