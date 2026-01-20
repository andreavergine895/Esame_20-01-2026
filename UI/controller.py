import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        try:
            self.n_album= int(self._view.txtNumAlbumMin.value)

        except ValueError:
            self._view.show_alert("Inserisci un numero valore numerico")
            return
        if self.n_album < 0:
            self._view.show_alert("Inserisci un numero valore numerico")
            return
        self._model.load_all_artists()
        self._model.load_artists_with_min_albums(self.n_album)
        self._model.build_graph()
        n_nodi, n_archi = self._model.get_graph_info()
        self._view.btnArtistsConnected.disabled = False
        self._view.ddArtist.disabled = False
        self.populate_dd(e)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f" il grafo ha {n_nodi} nodi e {n_archi} archi"))
        self._view.update_page()

    def populate_dd(self, e):
        self.nodi= self._model.nodes
        self._view.ddArtist.options.clear()
        for nodo in self.nodi:
            self._view.ddArtist.options.append(ft.dropdown.Option(f"{nodo.name}"))


    def get_selected_dd(self,e):
        nodo_sel= e.control.value
        self.nodo_sel= next((n for n in self._model.nodes if n.name == nodo_sel),None)


    def handle_connected_artists(self, e):
        lista= self._model.get_parte_connessa(self.nodo_sel)
        self._view.txt_result.controls.clear()
        for elemento in lista:
            self._view.txt_result.controls.append(ft.Text(f"artista {elemento[0]}, peso {elemento[1]}"))
        self._view.update_page()


