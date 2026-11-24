# Proyecto de fibra optica - Algoritmo de Kruskal
Proyecto separado en modulos y conectado a **MySQL**.

## Archivos
- `base_datos.py`: conexion con MySQL, consulta de localidades y tramos, y guardado de resultados.
- `grafo.py`: clases `Localidad`, `Tramo` y `Grafo`.
- `kruskal.py`: estructura Union-Find y algoritmo de Kruskal.
- `main.py`: ejecuta el proyecto y muestra el resultado.
- `schema.sql`: esquema de tablas y datos iniciales (si necesitas recrear la base).


## Configuracion
Abre `main.py` y ajusta estos valores según tu instalacion de MySQL:

```python
host="127.0.0.1"
puerto=3306
usuario="root"
clave=""
base_datos="fibra_optica"
```

## Ejecucion
Desde la terminal, ubicado en la carpeta del proyecto (powershell):

py main.py