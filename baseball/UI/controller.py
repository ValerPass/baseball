import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        if self._view._ddAnno.value is None:
            self._view._txt_result.controls.append(ft.Text(f"Seleziona un anno dal menù"))
            return
        self._model.buildGraph(self._view._ddAnno.value)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        nodi, archi = self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {nodi} nodi e {archi} archi"))
        self._view.update_page()

    def handleDettagli(self, e):
        v0 = self.selectedTeam
        vicini = self._model.getSortedNeighbors(v0)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Stampo i vicini di {v0} con relativo peso dell'arco"))
        for v in vicini:
            self._view._txt_result.controls.append(ft.Text(f"{v[1]} - {v[0]}"))
        self._view.update_page()

    def handlePercorso(self, e):
        pass

    def fillDDYear(self):
        years = self._model.getYears() #lista di oggetti
        yearsDD = map(lambda x: ft.dropdown.Option(x), years) #col metodo map applico la funzione a tutti gli elementi

        self._view._ddAnno.options = yearsDD
        self._view.update_page()

    def handleDDYearSelection(self, e):
        teams = self._model.getTeamsOfYear(self._view._ddAnno.value)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"Ho trovato {len(teams)} squadre che hanno giocato nell'anno {self._view._ddAnno.value}"))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f'{t.teamCode}'))
            #metodo per leggere il dropdown delle squadre che appaiono quando seleziono anno
            self._view._ddSquadra.options.append(ft.dropdown.Option(
                data=t,
                on_click=self.readDDTeam,
                text=t.teamCode,
            ))

        self._view.update_page()

    def readDDTeam(self, e):
        if e.control.data is None:
            self.selectedTeam = None
        else:
            self.selectedTeam = e.control.data
        print(f"readDDTeams called -- {self.selectedTeam}")