# MDC Online Class Attender

This bot can automatically join online classes that are held in [MDC BlackBoard Collaborate](https://mdc.blackboard.com/). The bot will join the class according to the given schedule. You could use this bot if your proffesors put the link of the classes in BlackBoard. If you have to join the classes by a link sent from the proffesor you could use this project as a guide and create your own bot. 

## Configure
There are a couple of thing you need to configure before running the bot:
1. Open bot.py, and put your MDC credentials in the CREDS dictionary.
* Example - ```CREDS = {'email' : 'myemail@gmail.com', 'passwd': 'mypassword'}```
2. In the same file you will have to change or add the names of how your profesors call the virtual room link.
* Example - ```common_names = ['VIRTUAL ROOM', 'BB Coll Ultra']```
3. Make sure that the timezone of the computer is correct.

## Installation
* Clone the repository locally ```https://github.com/javier-arango/class-attender-bot```


## Technologies
Project is created with:
* Python version: 3.7.5
* Selenium version: 3.141.0
* Schedule version: 0.6.0


## Attention
**This project is for educational purposes only - I will no be responsible for any issues related to your attendance or anything about your class**. I create this bot to learn how to use [selenium webdriver](https://www.selenium.dev) automation tools for the Chrome browser.
