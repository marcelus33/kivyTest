import json
import urllib.request

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp


def get_images(cantidad_imagenes=10):
    """ Función que consume una API para obtener imágenes """
    url = 'https://picsum.photos/v2/list?limit={}'.format(cantidad_imagenes)
    images = []
    try:
        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            print(data)
            for img in data:
                url = img.get('download_url')
                author = img.get('author')
                print(url)
                images.append((url, author))
    except Exception as e:
        print(e)
    # se devuelve un listado de tuplas de (url, autor)
    return images


class ImageRow(GridLayout):
    source = ObjectProperty(None)
    name = ObjectProperty(None)


class Buscador(Screen):
    images = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        # Inicializamos con las imágenes de la API
        self.images = get_images(20)
        self.ids.rv.data = [{'source': str(x), 'name': str(y)} for x, y in self.images]

    def set_list_images(self, text="", search=False):
        """ Setea la lista de imagenes para el buscador """

        def add_image_item(name):
            self.ids.rv.data.append({"viewclass": "ImageRow", "name": name})

        self.ids.rv.data = []
        images_names = [y for x, y in self.images]
        for image_name in images_names:
            if search:
                if text.lower() in image_name.lower():
                    add_image_item(image_name)
            else:
                add_image_item(image_name)


Builder.load_file('image.kv')


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Buscador'
        self.screen = Buscador()

    def build(self):
        return self.screen


MainApp().run()

