from jinja2 import Template


class Message:
    def __init__(self, text):
        self.text = text

    def render(self, **kwargs):
        return Template(self.text).render(**kwargs)
