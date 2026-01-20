import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.artists_list = []
        self.mappa_id = {}
        self.load_all_artists()
        self.nodes=[]

        self.archi=None


    def load_all_artists(self):
        self.artists_list = DAO.get_all_artists()
        for a in self.artists_list:
            self.mappa_id[a.id] = a

        print(f"Artisti: {self.artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self.nodes= DAO.get_artist_min_album(min_albums, self.mappa_id)


    def build_graph(self):
        self._graph.clear()
        self._graph.add_nodes_from(self.nodes)
        self.archi= DAO.get_artist_connessi(self.mappa_id)
        archi_filtrati=[]
        for u, v, peso in self.archi:
            if u in self._graph and v in self._graph:
                archi_filtrati.append((u, v, peso))
        self._graph.add_weighted_edges_from(archi_filtrati)

    def get_graph_info(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def get_parte_connessa(self, artista):
        self.parte_connesa =  self._graph.neighbors(artista)
        lista_tuple_nodo_peso = []
        for nodo in self.parte_connesa:
            peso= self._graph[artista][nodo]["weight"]
            lista_tuple_nodo_peso.append((nodo, peso))
        lista_tuple_nodo_peso.sort(key=lambda x: x[1])
        return lista_tuple_nodo_peso

    def cerca_cammino(self):
        pass

    def ricorsione(self):
        pass




