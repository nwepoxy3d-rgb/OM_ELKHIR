"""
OM EL KHIR — première base Android
Application d'aide à l'observation de signes archéologiques à partir de photos.

Cette version permet de tester l'interface, l'aperçu caméra et l'importation
d'une image. Elle ne prétend pas encore interpréter automatiquement les signes.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.camera import Camera  # Register Camera widget for the KV layout
from kivy.uix.image import Image
from kivy.utils import platform

KV = """
ScreenManager:
    HomeScreen:
    CameraScreen:
    ImageScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: "24dp"
        spacing: "18dp"
        canvas.before:
            Color:
                rgba: 0.055, 0.075, 0.10, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "OM EL KHIR"
            font_size: "30sp"
            bold: True
            color: 0.88, 0.78, 0.53, 1
            size_hint_y: None
            height: "64dp"
        Label:
            text: "Observation et documentation des signes"
            font_size: "16sp"
            color: 0.88, 0.90, 0.93, 1
            size_hint_y: None
            height: "48dp"
        Widget:
        Button:
            text: "OUVRIR LA CAMÉRA"
            size_hint_y: None
            height: "54dp"
            background_normal: ""
            background_color: 0.20, 0.35, 0.43, 1
            on_release: app.open_camera()
        Button:
            text: "IMPORTER UNE PHOTO"
            size_hint_y: None
            height: "54dp"
            background_normal: ""
            background_color: 0.35, 0.31, 0.22, 1
            on_release: app.open_image_picker()
        Label:
            text: "Version de démarrage — moteur d'analyse à construire"
            font_size: "12sp"
            color: 0.62, 0.67, 0.72, 1
            size_hint_y: None
            height: "36dp"

<CameraScreen>:
    name: "camera"
    BoxLayout:
        orientation: "vertical"
        padding: "12dp"
        spacing: "10dp"
        Label:
            text: "APERÇU CAMÉRA"
            size_hint_y: None
            height: "42dp"
            bold: True
        Camera:
            id: camera_preview
            resolution: (1280, 720)
            play: True
        Button:
            text: "RETOUR"
            size_hint_y: None
            height: "50dp"
            on_release: app.close_camera()

<ImageScreen>:
    name: "image"
    BoxLayout:
        orientation: "vertical"
        padding: "12dp"
        spacing: "10dp"
        Label:
            text: "PHOTO SÉLECTIONNÉE"
            size_hint_y: None
            height: "42dp"
            bold: True
        Image:
            id: selected_image
            source: root.image_path
            fit_mode: "contain"
        Label:
            text: root.status_text
            size_hint_y: None
            height: "44dp"
            text_size: self.width, None
            halign: "center"
        Button:
            text: "RETOUR À L'ACCUEIL"
            size_hint_y: None
            height: "50dp"
            on_release: app.go_home()
"""

class HomeScreen(Screen):
    pass


class CameraScreen(Screen):
    pass


class ImageScreen(Screen):
    image_path = StringProperty("")
    status_text = StringProperty(
        "L'image est chargée. L'analyse scientifique sera ajoutée dans une prochaine étape."
    )


class OmElkhirApp(App):
    def build(self):
        self.title = "OM EL KHIR"
        root = Builder.load_string(KV)
        return root

    def on_start(self):
        if platform == "android":
            try:
                from android.permissions import Permission, request_permissions
                request_permissions([Permission.CAMERA])
            except Exception:
                # L'application reste utilisable même si la demande échoue.
                pass

    def open_camera(self):
        self.root.current = "camera"

    def close_camera(self):
        camera_screen = self.root.get_screen("camera")
        camera_screen.ids.camera_preview.play = False
        self.root.current = "home"

    def open_image_picker(self):
        try:
            from plyer import filechooser
            filechooser.open_file(
                on_selection=self.on_image_selected,
                filters=[("Images", "*.png", "*.jpg", "*.jpeg", "*.webp")]
            )
        except Exception as exc:
            image_screen = self.root.get_screen("image")
            image_screen.status_text = "Sélecteur de fichiers indisponible : " + str(exc)
            self.root.current = "image"

    def on_image_selected(self, selection):
        if not selection:
            return
        path = selection[0]
        image_screen = self.root.get_screen("image")
        image_screen.image_path = path
        image_screen.status_text = (
            "Photo importée. Aucune interprétation automatique n'est encore activée."
        )
        self.root.current = "image"

    def go_home(self):
        self.root.current = "home"


if __name__ == "__main__":
    OmElkhirApp().run()
