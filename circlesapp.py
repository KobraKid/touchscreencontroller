from kivy.app import App
from kivy.uix.widget import Widget


class CirclesGame(Widget):
    pass


class CirclesApp(App):
    def build(self):
        return CirclesGame()


if __name__ == '__main__':
    CirclesApp().run()
