# Invera ToDo-List Challenge 
> Python/Django Jr-SSr

# Tabla de contenidos

- [Invera ToDo-List Challenge](#invera-todo-list-challenge)
- [Tabla de contenidos](#tabla-de-contenidos)
- [Enunciado](#enunciado)
  - [Qué queremos que hagas:](#qué-queremos-que-hagas)
  - [Objetivos:](#objetivos)
  - [Qué evaluamos:](#qué-evaluamos)
  - [Requerimientos de entrega:](#requerimientos-de-entrega)
- [Levantar localmente](#levantar-localmente)
  - [Correr directamente](#correr-directamente)

# Enunciado

El propósito de esta prueba es conocer tu capacidad para crear una pequeña aplicación funcional en un límite de tiempo. A continuación, encontrarás las funciones, los requisitos y los puntos clave que debés tener en cuenta durante el desarrollo.

## Qué queremos que hagas:

- El Challenge consiste en crear una aplicación web sencilla que permita a los usuarios crear y mantener una lista de tareas.
- La entrega del resultado será en un nuevo fork de este repo y deberás hacer una pequeña demo del funcionamiento y desarrollo del proyecto ante un super comité de las más grandes mentes maestras de Invera, o a un par de devs, lo que sea más fácil de conseguir.
- Podes contactarnos en caso que tengas alguna consulta.

## Objetivos:

El usuario de la aplicación tiene que ser capaz de:

- Crear una tarea
- Eliminar una tarea
- Marcar tareas como completadas
- Poder ver una lista de todas las tareas existentes
- Filtrar/buscar tareas por fecha de creación y/o por el contenido de la misma

## Qué evaluamos:

- Desarrollo utilizando Python, Django. No es necesario crear un Front-End, pero sí es necesario tener una API que permita cumplir con los objetivos de arriba.
- Calidad y arquitectura de código. Facilidad de lectura y mantenimiento del código. Estándares seguidos.
- [Bonus] Manejo de logs.
- [Bonus] Creación de tests (unitarias y de integración)
- [Bonus] Unificar la solución propuesta en una imagen de Docker por repositorio para poder ser ejecutada en cualquier ambiente (si aplica para full stack).

## Requerimientos de entrega:

- Hacer un fork del proyecto y pushearlo en github. Puede ser privado.
- La solución debe correr correctamente.
- El Readme debe contener todas las instrucciones para poder levantar la aplicación, en caso de ser necesario, y explicar cómo se usa.
- Disponibilidad para realizar una pequeña demo del proyecto al finalizar el challenge.
- Tiempo para la entrega: Aproximadamente 7 días.

# Levantar localmente

## Correr directamente

Crear venv e instalar requisitos:

```bash
python3 -m venv venv_invera_todo
source venv_invera_todo/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Levantar server

```bash
python manage.py runserver
```