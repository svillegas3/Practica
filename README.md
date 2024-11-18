# FUNCIONAMIENTO:

### (A) 
Los únicos archivos a manejar son dos, `app.py` y `comandos.py`
   (Sin embargo, `comandos.py` solo se usa como si fuera un programa exclusivo de administrador, ya que permite modificar la lista de libros de la biblioteca)

### (B) 
Pasos para ejecutar este código:
   - Abrir este directorio en **VS Code** u otro editor de código.
   - Abrir la terminal y escribir `python app.py`.
   - Opcionalmente, abrir la terminal y escribir `python comandos.py` y seguir las indicaciones dentro de este archivo para modificar la lista de libros.
   - Instalar las siguientes librerías usando estos comandos:
     ```bash
     pip install ast
     pip install os  # (puede que venga por defecto)
     pip install re  # (puede que venga por defecto)
     pip install random  # (puede que venga por defecto)
     pip install termcolor
     pip install networkx
     pip install matplotlib
     pip install numpy
     pip install pyinstaller
     ```

### (C) 
Se puede usar el comando 'pyinstaller --onefile app.py' en la terminal para crear un ejecutable (el cual se crea en una carpeta dist). Sin embargo, la lista de libros
no se podría modificar nuevamente, quedaría definida como una constante.