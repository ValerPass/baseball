import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._allTeams = []
        self._grafo = nx.Graph()
        self.idMapTeams = {}

    def buildGraph(self, year):
        self._grafo.clear()

        #costruisco il grafo
        if len(self._allTeams)==0:
            print("Lista squadre vuota")
            return
        # ha come nodi i teams
        self._grafo.add_nodes_from(self._allTeams)

        #arco fra qualsiasi nodo
        for t1 in self._grafo.nodes:
            for t2 in self._grafo.nodes:
                if t1 != t2:
                    self._grafo.add_edge(t1, t2)

        # Modo 2 - usando la libreria itertools di Python, che fornisce una serie di metodi comodi per lavorare sugli iteratori.
        # Possiamo usare il metodo .combinations(), che ci restituisce le combinazioni degli elementi di una lista che gli passiamo
        # come argomento. Questo ci permette di non avere ripetizioni, quindi se ho (a,b) non potrò avere (b,a).

        #myedges = list(itertools.combinations(self._allTems,2)) #lista di tuple(nodoP, nodoA)
        #self._grafo.add_edges_from(myedges)

        #AGGIUNGERE I PESI FACENDO UNA QUERY

        #il peso di ciascun arco è la somma dei salari dei giocatori delle 2 squadre (collegate dall'arco) nell'anno scelto
        salariesOfTeams = DAO.getSalaryOfTeams(year, self.idMapTeams)

        for e in self._grafo.edges:
            self._grafo[e[0]][e[1]]["weight"] = salariesOfTeams[e[0]]+salariesOfTeams[e[1]] #somma dei salari di quella squadra

    def getYears(self):
        return DAO.getAllYears()

    def getTeamsOfYear(self, year):
        self._allTeams = DAO.getTeamsOfYear(year)
        self.idMapTeams = {t.ID: t for t in self._allTeams} #dizionario ch associa l'ID del team all'oggetto team
        return self._allTeams

    def getGraphDetails(self):
       return len(self._grafo.nodes), len(self._grafo.edges)

    def printGraphDetails(self):
        print(f"Grafo creato con {len(self._grafo.nodes)} nodi e {len(self._grafo.edges)} archi")

    def getSortedNeighbors(self, v0):
        vicini = self._grafo.neighbors(v0)
        viciniTuple = []
        for v in vicini:
            viciniTuple.append( (v, self._grafo[v0][v]["weight"]) )

        viciniTuple.sort(key=lambda x: x[1], reverse=True)
        return viciniTuple