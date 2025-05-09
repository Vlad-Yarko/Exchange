from ..messages.message import Message


code_message = Message("""
Hello {{ username }}
Here is your code
{{ code }}
Do not give it to third party
""")


crypto_message = Message("""
Crypto
{{ symbol }} - {{ price }}
""")


currency_message = Message("""
Currency
{{ symbol }} - {{ price }}
""")
