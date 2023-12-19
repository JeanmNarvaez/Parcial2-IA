import numpy as np

class Nodo:
   def __init__(self, nombre, padre, arista=None):
       self.nombre = nombre
       self.padre = padre
       self.hijos = []
       self.arista = arista

   def agregar_hijo(self, hijo):
       self.hijos.append(hijo)

   def regresar_hijo(self, arista):
       for hijo in self.hijos:
           if hijo.arista == arista:
               return hijo
       return None

class ID3_C:
   def __init__(self):
       self.raiz = None
       self.atributos = None
       self.datos = None

   def crear_nodo(self, nombre, padre, arista=None):
       return Nodo(nombre, padre, arista)

   def establecer_atributos(self, atributos):
       self.atributos = atributos

   def instancia_mas_abundante(self, Y):
       unicos, cuenta = np.unique(Y, return_counts=True)
       cuenta = cuenta.tolist()
       return unicos[cuenta.index(max(cuenta))]

   def petalo(self, X, Y):
       if self.atributos is None:
           self.atributos = [f"Atributos_{i}" for i in range(X.shape[1])]

       if np.all(Y == Y[0]):
           self.raiz = self.crear_nodo(Y[0], None)
       else:
           atributo = self.seleccionar_atributo(X, Y, [])
           nombre_raiz = self.atributos[atributo]
           self.raiz = self.crear_nodo(nombre_raiz, None)
           self.encontrar_hijos(X, Y, atributo, [atributo], self.raiz)

   def encontrar_hijos(self, X, Y, atributo, antecedente, nodo_actual):
       columna_atributo = X[:, atributo]
       valores_unicos = np.unique(columna_atributo).tolist()

       for valor in valores_unicos:
           x = X[columna_atributo == valor]
           y = Y[columna_atributo == valor]

           if len(antecedente) == X.shape[1]:
               instancia = self.instancia_mas_abundante(y)
               hijo = self.crear_nodo(instancia, nodo_actual, valor)
               nodo_actual.agregar_hijo(hijo)
           elif np.all(y == y[0]):
               hijo = self.crear_nodo(y[0], nodo_actual, valor)
               nodo_actual.agregar_hijo(hijo)
           else:
               hijo = self.seleccionar_atributo(x, y, antecedente)
               nombre_hijo = self.atributos[hijo]
               nodo_hijo = self.crear_nodo(nombre_hijo, nodo_actual, valor)
               nodo_actual.agregar_hijo(nodo_hijo)
               self.encontrar_hijos(x, y, hijo, antecedente + [hijo], nodo_hijo)

   def seleccionar_atributo(self, X, Y, antecedente):
       ganancia = []

       for i, atributo in enumerate(X.T):
           if i not in antecedente:
               ganancia.append(self.calcular_ganancia(atributo, Y))
           else:
               ganancia.append(float("-inf"))
       return ganancia.index(max(ganancia))

   def calcular_ganancia(self, atributo, Y):
       entropia_atributos = 0

       for valor in np.unique(atributo):
           y = Y[atributo == valor]
           proporcion = y.size / Y.size
           entropia_atributos += proporcion * self.calcular_entropia(y)

       ganancia = self.calcular_entropia(Y) - entropia_atributos
       return ganancia

   def calcular_entropia(self, Y):
       entropia = 0

       for valor in np.unique(Y):
           y = Y[Y == valor]
           proporcion = y.size / Y.size
           entropia -= proporcion * np.log2(proporcion)

       return entropia

   def predecir(self, X):
       Y = np.empty(X.shape[0], dtype="<U30")

       for i, fila in enumerate(X):
           Y[i] = self.predecir_fila(fila)

       return Y

   def predecir_fila(self, fila):
       nodo_actual = self.raiz

       while nodo_actual.hijos:
           atributo = nodo_actual.nombre
           columna_atributo = self.atributos.index(atributo)
           valor_atributo = fila[columna_atributo]
           nodo_actual = nodo_actual.regresar_hijo(valor_atributo)

       return nodo_actual.nombre

   def imprimir_arbol(self, nodo_actual, nivel=0):
       if nodo_actual is not None:
           print("  " * nivel + f"{nodo_actual.nombre} ({nodo_actual.arista})")
           for hijo in nodo_actual.hijos:
               self.imprimir_arbol(hijo, nivel + 1)

   def porcentaje_atributos(self, datos):
       num_filas = datos.shape[0]
       num_columnas = datos.shape[1]

       for i in range(num_columnas):
           unique, counts = np.unique(datos[:, i], return_counts=True)
           print(f"Atributo {i + 1}:")
           for value, count in zip(unique, counts):
               percentage = (count / num_filas) * 100
               print(f"  Valor: {value}, Porcentaje: {percentage:.2f}%")
           print()



   def informacion_variables(self):
       if self.datos is None:
           print("Error: No se han proporcionado datos.")
           return

       print("Los datos han sido cargados correctamente.")

       num_filas = self.datos.shape[0]
       num_columnas = self.datos.shape[1]
       print(f"El conjunto de datos tiene {num_filas} filas y {num_columnas} columnas.")

       for i in range(num_columnas - 1):  # Excluir la última columna (clase)
           unique, counts = np.unique(self.datos[:, i], return_counts=True)
           entropy = 0
           total_instances = sum(counts)
           for count in counts:
               probability = count / total_instances
               entropy -= probability * np.log2(probability)
           ganancia = self.calcular_ganancia(self.datos[:, i], self.datos[:, -1])
           print(f"Variable {i + 1}: Entropía: {entropy:.4f}, Ganancia: {ganancia:.4f}")


# Cargar datos de pétalos desde un archivo CSV
datos = np.genfromtxt('C:\\Jean 2023\\Other\\breast-cancer.csv', delimiter=",", dtype="str")

# Separar atributos y clases
X = datos[:, :-1]
Y = datos[:, -1]

# Crear y petalo el árbol
arbol = ID3_C()
arbol.petalo(X, Y)
arbol.datos = datos

# Imprimir la estructura del árbol
print("arbol de decisiones:")
arbol.imprimir_arbol(arbol.raiz)

print("Porcentaje de cada atributo en los datos:")
arbol.porcentaje_atributos(datos)

# Calcula la información de cada variable en el conjunto de datos
print("Información de cada variable:")
arbol.informacion_variables()

# Realizar predicciones y calcular el porcentaje de aciertos
salida = arbol.predecir(X)
accuracy = 100 * sum(Y == salida) / X.shape[0]
print('Aciertos: ', accuracy)

