# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 20:45:30 2019

@author: DRMD_
Juego de gato sin GUI usando minimax.
"""
"""
Se hacen importaciones, se declaran las constantes.
"""

from math import inf

""" Estados Finales."""
GANAX = 'Gana X'
GANAO = 'Gana O'
EMPATE = 'Empate'


##################################################################################################
class Juego():
    """ Se define el juego."""

    def __init__(self):  
        self.profundidad = 9
        self.jugadores= ['X', 'O']
        self.tablero = [[{"pos": 0, "valor": 0} for y in range(0, 3)] for x in range(0, 3)]
        pos = 0
        
        for fila in self.tablero:
            for casilla in fila:
                pos += 1
                casilla["pos"] = pos
        
        
    def esta_lleno(self):
        """ Verifica si el tablero se encuentra lleno."""
        return [[casilla["pos"] for casilla in fila if casilla["valor"] is 0] for fila in self.tablero]
  
    
    def mover(self, jugador, pos):
        for fila in self.tablero:
            for casilla in fila:
                if casilla["pos"] is pos:
                    if casilla["valor"] is 0:
                        if jugador == 'X':
                            casilla["valor"] = 1
                            self.profundidad -= 1
                            return None
                        elif jugador == 'O':
                            casilla["valor"] = -1
                            self.profundidad -= 1
                            return None
                        else:
                            raise Exception("Jugador {} no válido.".format(jugador))
                    else:
                        raise Exception("{} es un movimiento no válido".format(pos))
        raise Exception("Fuera de los límites.")
    
    
    def deshacer(self, jugador, pos):
        for fila in self.tablero:
            for casilla in fila:
                if casilla["pos"] is pos:
                    if casilla["valor"] is not 0:
                        casilla["valor"] = 0
                        self.profundidad += 1
                    else:
                        raise Exception("No se puede deshacer {} .".format(pos))
        
    
    def puntos(self):
        verticales = [[fila[i]["valor"] for fila in self.tablero] for i in range(len(self.tablero))]
        indice = 2
        diagonales = [[self.tablero[num][num]["valor"] for num in range(0, 3)], [self.tablero[num][indice - num]["valor"] for num in range(0, 3)]]
        posibilidad_triunfo = []
        posibilidad_triunfo.append([[casilla["valor"] for casilla in fila] for fila in self.tablero])
        posibilidad_triunfo.append(verticales)
        posibilidad_triunfo.append(diagonales)
        
        for posibilidad in posibilidad_triunfo:
            for fila in posibilidad:
                if sum(fila) is 3:
                    return 5
                elif sum(fila) is -3:
                    return -5
        return 0
    
    
    def fin_juego(self):
        if self.puntos() > 0 or self.profundidad <= 0 or self.puntos() < 0:
            return True
        else:
            return False


##################################################################################################
class Minimax():
    """Algoritmo Minimax. """
    def minimax(self, estado, profundidad, alpha, beta, maxv):
        if estado.fin_juego() or profundidad is 0:
            return -1, estado.puntos() - profundidad
        
        if maxv:
            mejor_valor = -1, -inf
        else:
            mejor_valor = -1, inf
        
        for t in self.proximos_mov(estado):
            jugador = 'X' if maxv else 'O'
            estado.mover(jugador, t)
            valor = t, self.minimax(estado, int(profundidad - 1), alpha, beta, not maxv)[1]
            estado.deshacer(jugador, t)
            
            if maxv:
                mejor_valor = max(mejor_valor, valor, key= lambda i: i[1])
                alpha = max(alpha, mejor_valor[1])
                if alpha >= beta:
                    break
            else:
                mejor_valor = min(mejor_valor, valor, key= lambda i: i[1])
                beta = min(beta, valor[1])
                if alpha >= beta:
                    break
        return mejor_valor
    
    
    def proximos_mov(self, estado):
        movimientos = []
        for fila in estado.esta_lleno():
            for casilla in fila:
                movimientos.append(casilla)
        return movimientos
    
    
    def evaluar(self, estado):
        return estado.puntos
    
    
    def elegir(self, estado, jugador):
        return self.minimax(estado, len(self.proximos_mov(estado)), -inf, inf, jugador)


##################################################################################################
class Vista():
	def __init__(self, estado):
		self.estado_actual = estado
		self.estado_inicial = estado
		self.cuadricula ="\n\n"
		for fila in self.estado_actual.tablero:
			for casilla in fila:
				self.cuadricula +="| {} |".format(casilla["pos"])
			self.cuadricula += "\n"
		self.cuadricula += "\n"

	def dibujar(self):
		self.cuadro = ""		
		for fila in self.estado_actual.tablero:
			for casilla in fila:
				if casilla["valor"] is not 0:
					self.cuadro +="| {} |".format('X' if casilla["valor"] is 1 else 'O')
				else:
					self.cuadro +="|   |"
			self.cuadro += "\n"
		return self.cuadro


def main(vista, alg):
    jugador = 1
    print("Numero de casillas a jugar", vista.cuadricula)
    print(vista.dibujar())
    while not vista.estado_actual.fin_juego():
        var = 'X' if jugador is 1 else 'O'
        print(" **********************************************************************************\n\n")
        movimiento = 0
        if jugador is 1:
            movimiento = input("\n Turno de Jugador - {} :' \n ".format(var))
        else:
            print("Turno de Jugador - O : \n")
            movimiento = alg.elegir(vista.estado_actual, False)[0]
        vista.estado_actual.mover(var, int(movimiento))
        print(" **********************************************************************************")
        print(vista.dibujar())
        print("Movimientos restantes ",vista.estado_actual.esta_lleno())
        jugador = -jugador
    if vista.estado_actual.puntos() == 5:
        print(GANAX)
    elif vista.estado_actual.puntos() == -5:
        print(GANAO)
    else:
        print(EMPATE)


##################################################################################################
if __name__ == '__main__':
    juego = Juego()
    tablero= Vista(juego)
    alg = Minimax()
    main(tablero, alg)
    
    
    
    
    
    
    
    
    
    
    
    
    
    

