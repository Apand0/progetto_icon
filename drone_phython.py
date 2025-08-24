from os import path


class Drone:
    def _init_(self,nome, scelta_batteria, speed):
        self.x = "41°11′45.96″N"
        self.y = "41°11′45.96″N"                                                                                                                             
        self.z= "0"
        self.scelta_batteria=scelta_batteria
        self.speed = speed

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def move_up(self):
        self.z -= self.speed

    def move_down(self):
        self.z += self.speed


    def move_forward(self):
        self.y -= self.speed

    def move_back(self):
        self.y += self.speed
    
    def run(self, kb):
        self.kb = kb
        path, tempo = self.traccia_percorso()
        self.salta(20)
        effettuate = self.sposta(path)
        return path, effettuate
        