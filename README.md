# Online Class Attender :robot:
> Class Attender

This bot can automatically join online classes that are held in [BlackBoard Collaborate](https://mdc.blackboard.com/). The bot will join the class according to the given schedule. You could use this bot if your professors put the link of the classes in BlackBoard. If you have to join the classes by a link sent from the professor you could use this project as a guide and create your bot. 

## Instruction :notebook:
* The first thing that the bot is going to ask you is about entering info about your class schedule. Please provide the correct and exact data that the bot asks you. Here is a [website](https://www.ontheclock.com/convert-military-24-hour-time.aspx) if you don't know how to change standard time to military time 
* After you enter the correct data the bot will create a schedule.db file that will be your schedule database. If you put incorrect data you will have to delete the file and run the bot again. (This could be improved so you don't have to do this)
* The bot will join and leave the class for you if everything is correct.

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
* **This project is for educational purposes only - I will no be responsible for any issues related to your attendance or anything about your class**.
* If you install any python library on your computer it is recommended that you do it in a virtual environment. Please check [Anaconda virtual environment](https://www.anaconda.com) for more information on how to create one.
* I recommend that you run the bot in a virtual machine or on a computer that is always on. If you run the bot multiple times you will have to delete the schedule.db file before running it because if you don't do it it will give you an error or the bot will not run well. You can use [Microsoft Azure](https://azure.microsoft.com/en-us/services/virtual-machines/) to create a free virtual machine.
* Please if you find any error or you can't run the bot just leave a comment or send me an email and I will try to fix it. This project is not finished and it could be improved. I will try my best to fix everything and to make it better. 
