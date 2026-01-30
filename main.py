# 1. SETUP ENVIRONMENT & TOOLS
!sudo apt-get update
!sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev libtool automake autoconf zlib1g-dev ncurses-dev cmake
!pip install --upgrade pip
!pip install Cython==0.29.33 buildozer

# 2. MASTER SOURCE CODE (OPTIMIZED FOR PERFORMANCE)
main_py_content = """
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.filechooser import FileChooserIconView

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="OM ELKHIR SYSTEM v2.0", font_size='24sp', size_hint_y=0.2))
        
        btn_scan = Button(text="OPEN FIELD SCANNER", background_color=(0, 0.8, 0, 1))
        btn_scan.bind(on_press=self.go_to_scan)
        
        btn_load = Button(text="LOAD IMAGE ANALYSIS", background_color=(0, 0.5, 0.8, 1))
        btn_load.bind(on_press=self.go_to_load)
        
        layout.add_widget(btn_scan)
        layout.add_widget(btn_load)
        self.add_widget(layout)

    def go_to_scan(self, instance):
        self.manager.current = 'scanner'

    def go_to_load(self, instance):
        self.manager.current = 'loader'

class ScannerScreen(Screen):
    def on_enter(self):
        layout = BoxLayout(orientation='vertical')
        self.cam = Camera(play=True, resolution=(640, 480))
        btn_back = Button(text="BACK TO MENU", size_hint_y=0.2)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(self.cam)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def go_back(self, instance):
        self.cam.play = False
        self.manager.current = 'menu'

class LoaderScreen(Screen):
    def on_enter(self):
        layout = BoxLayout(orientation='vertical')
        file_chooser = FileChooserIconView()
        btn_back = Button(text="BACK TO MENU", size_hint_y=0.1)
        btn_back.bind(on_press=self.go_back)
        layout.add_widget(file_chooser)
        layout.add_widget(btn_back)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'menu'

class OmElkhirApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ScannerScreen(name='scanner'))
        sm.add_widget(LoaderScreen(name='loader'))
        return sm

if __name__ == '__main__':
    OmElkhirApp().run()
"""
with open('main.py', 'w') as f:
    f.write(main_py_content)

# 3. CONFIGURE PERMISSIONS (CRITICAL)
!buildozer init
!sed -i 's/#android.permissions = PACKAGE_NAME.PERMISSION/android.permissions = CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE/' buildozer.spec
!sed -i 's/requirements = python3,kivy/requirements = python3,kivy,opencv,numpy/' buildozer.spec

# 4. FINAL BUILD
!buildozer -v android debug
