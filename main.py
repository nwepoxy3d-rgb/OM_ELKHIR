from kivy.app import App
from kivy.uix.label import Label

class OmElkhir(App):
    def build(self):
        return Label(text='OM ELKHIR: System Active\nScanning for Voids...')

if __name__ == '__main__':
    OmElkhir().run()
