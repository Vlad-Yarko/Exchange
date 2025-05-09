from ..messages.message import Message


start_hand_message = Message("""
Hello {{ username }}
You are in exchange bot
/help
""")


help_hand_message = Message("""
So this telegram bot is official bot of website 'Exchange'
This bot is used for sending messages from site, so on site you subscribe on some currencies and here receive alerts
To connect your account here you can use /register 
""")


register_hand_message = Message("""
Click the button to share your phone number
""")
