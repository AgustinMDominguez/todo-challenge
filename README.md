# Invera ToDo-List Challenge
> Python/Django Jr-SSr

**Autor:** Agustín Marcelo Domínguez: `agustinmarcelodominguez@gmail.com`

**Fecha** Agosto 2021

# Tabla de contenidos

- [Invera ToDo-List Challenge](#invera-todo-list-challenge)
- [Tabla de contenidos](#tabla-de-contenidos)
- [Enunciado](#enunciado)
  - [Qué queremos que hagas](#qué-queremos-que-hagas)
  - [Objetivos](#objetivos)
  - [Qué evaluamos](#qué-evaluamos)
  - [Requerimientos de entrega](#requerimientos-de-entrega)
- [Levantar localmente](#levantar-localmente)
  - [Correr directamente](#correr-directamente)
  - [Docker](#docker)
  - [Postman](#postman)
- [Endpoints](#endpoints)
  - [Descripcion General](#descripcion-general)
  - [search-tasks](#search-tasks)
- [Estilo y estructura](#estilo-y-estructura)
- [Referencias Usadas](#referencias-usadas)
- [Problemas conocidos / posibles mejoras](#problemas-conocidos--posibles-mejoras)

# Enunciado

El propósito de esta prueba es conocer tu capacidad para crear una pequeña aplicación funcional en un límite de tiempo. A continuación, encontrarás las funciones, los requisitos y los puntos clave que debés tener en cuenta durante el desarrollo.

## Qué queremos que hagas

- El Challenge consiste en crear una aplicación web sencilla que permita a los usuarios crear y mantener una lista de tareas.
- La entrega del resultado será en un nuevo fork de este repo y deberás hacer una pequeña demo del funcionamiento y desarrollo del proyecto ante un super comité de las más grandes mentes maestras de Invera, o a un par de devs, lo que sea más fácil de conseguir.
- Podes contactarnos en caso que tengas alguna consulta.

## Objetivos

El usuario de la aplicación tiene que ser capaz de

- Crear una tarea
- Eliminar una tarea
- Marcar tareas como completadas
- Poder ver una lista de todas las tareas existentes
- Filtrar/buscar tareas por fecha de creación y/o por el contenido de la misma

## Qué evaluamos

- Desarrollo utilizando Python, Django. No es necesario crear un Front-End, pero sí es necesario tener una API que permita cumplir con los objetivos de arriba.
- Calidad y arquitectura de código. Facilidad de lectura y mantenimiento del código. Estándares seguidos.
- [Bonus] Manejo de logs.
- [Bonus] Creación de tests (unitarias y de integración)
- [Bonus] Unificar la solución propuesta en una imagen de Docker por repositorio para poder ser ejecutada en cualquier ambiente (si aplica para full stack).

## Requerimientos de entrega

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

## Docker
Correr:

```bash
docker-compose build && docker-compose up
```

Luego se le pueden hacer pedidos a `http://127.0.0.1:8000` (ver sección [Postman](#postman))

## Postman

Se provee una colección de [Postman](https://www.postman.com/) (el archivo llamado `postman_collection.json`) con ejemplos de los endpoints hechos para probar directamente.

Para usar la colección hay que abrir Postman y poner `import` -> `file` y seleccionar el archivo `postman_collection.json`.

Tener en cuenta que no se subió la base de datos por lo que luego de correrlo local hay que registrarse, hacer login, y actualizar el la variable de entorno `PROFILE_TOKEN` de la colección.
Una vez que se le pegue al endpoint `login` y se obtenga el token, hacer doble click en la colección, ir a `variables` y actualizar tanto `INITIAL VALUE` como `CURRENT VALUE` con el token obtenido. Luego hacer una llamada al endpoint `logged_in` debería devolver un 200 con información del usuario y perfil actual.

# Endpoints

**Todos los endpoints que piden un body es en formato json**

**Para los endpoints que son *POST* los tipos de los parámetros son parseados como en Javascript (ie. null, true, ...)**

**mientras que cuando los endpoints son *GET* los tipos son parseados como en Python (ie. None, True, ['apple'])**
**con la excepcion de `start_time` y `end_time` que pueden ser isoformat generado por js**

**Si un perfil es creado o actualizado, se actualiza el token que lo asocia por lo que las siguientes llamadas**
**a la API deben hacerse con el nuevo token, que se provee en el return de los respectivos endpoints, y**
**siempre se puede obtener del endpoint `login`**

## Descripcion General

| Type | Endpoint                            | Params/Body                                                             | Return                                                                                    |
|------|-------------------------------------|-------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| GET  | `/todo/up`                          | `None`                                                                  | `{"status": "ok"}`                                                                        |
| POST | `/todo/register`                    | `{"username": str, "email": str, "password": str}`                      | `{"status": "ok"}`                                                                        |
| POST | `/todo/login`                       | `{"username": str, "password": str}`                                    | `{"profiles": [{"name": str, "token": "ey..."}]}` Lista de perfiles con sus respectivos TOKEN para autenticar |
| GET  | `/todo/logged_in`                   | `None`                                                                  | `{"user": str, "profile": str}` si el token es aceptado                                  |
| POST | `/todo/create-profile`              | `{"name": str}`                                                         | `{"status": "ok", "result": {"name": str, "token": token}}`                               |
| POST | `/todo/rename-profile`              | `{"old_profile_name": str, "new_profile_name": str}`                    | `{"status": "ok", "result": {"name": str, "user": str, "token": token}}`                  |
| POST | `/todo/delete-profile`              | `{"profile_name": str}`                                                 | `{"status": "ok", "result": {"deleted": true}}`                                           |
| POST | `/todo/add-task`                    | OBLIGATORIO: `title` - OPCIONALES: `parent_id: int, description: str, done: bool, tags: list[str], favorite: bool,` | `{"status": "ok", "result": {"id": int, "parent_id": int, "title": str, "description": str, "done": bool, "favorite": bool, "created_at": datetime}}` |
| GET  | `/todo/search-tasks`                | Ver [search-tasks](#search-tasks) | `{"status": "ok", "result": {"amount": int, "tasks": [task...]}}`                         |
| POST | `/todo/task/<int:task_id>/done`     | `{"done": bool}`                                                        | `{"status": "ok", "result": {"id": int, "parent_id": int, "title": str, "description": str, "done": bool, "favorite": bool, "created_at": datetime}}` |
| POST | `/todo/task/<int:task_id>/update`   | Se pueden actualizar opcionalmente: `title: str, parent_id: int, description: str, done: bool, tags: list[str], favorite: bool` | `{"status": "ok", "result": {"id": int, "parent_id": int, "title": str, "description": str, "done": bool, "favorite": bool, "created_at": datetime}}` |
| POST | `/todo/task/<int:task_id>/delete`   | `None`                         | `{"status": "ok", "result": {"deleted": true}}`                                           |
| GET  | `/todo/task/<int:task_id>/children` | Mismos campos que `search-tasks` pero limitado a subtareas de task_id  | `{"status": "ok", "result": {"tasks": [task...]}}`                  |


## search-tasks

Como es una `GET Request` los argumentos de filtro se pasan como parámetros. Por ejemplo:

`/todo/search-tasks?search_sub_tree=True&done=False&parent_id=9&tags=["apple", "some"]`

Los posibles parametros (todos opcionales) que se le pueden pasar
son primero los campos basicos del modelo (con excepción de descripción):

 * `done : str` - Para filtrar las tareas completas o no
 * `title : str` - En este caso tiene que ser un match exacto
 * `parent_id : int` - El id de otra task, por lo que limita la búsqueda a las subtareas de esta (se puede hacer el mismo comportamiento con `/todo/task/<int:task_id>/children`)
 * `tags : list[str]` - Un filtro de OR inclusivo para las tareas que se crearon con esas tags.
 * `favorite : bool` - Filtra a tareas que exclusivamente fueron marcadas como favoritas (o no)

Luego hay unos argumentos especiales (no menos opcionales) para esta request que modifican la búsqueda. Estos son:

 * `start_time : datetime` - Se parsea con `iso8601` y filtra las tareas creadas despues de esta datetime
 * `end_time : datetime` - Se parsea con `iso8601` y filtra las tareas creadas antes de esta datetime
 * `page : int` - Por defecto existe una paginación con 50 tareas por pagina, por lo que si una búsqueda particular devuelve muchos elementos, se puede user este argumento para paginar
 * `search_sub_tree : bool` - Si este valor es falso (por defecto), la request filtrará solo por tareas sin madre (no devuelve subtareas)

# Estilo y estructura

Se siguió la estructura recomendada y default de los projectos de django, con estilos de PEP8 para el estilo de codigo
con ayuda de la herramienta `pycodestyle`

```bash
pycodestyle . --exclude=venv_*,**migrations**
```

# Referencias Usadas

 - [Usar tokens para autenticacion en Django](https://www.django-rest-framework.org/api-guide/authentication/#setting-the-authentication-scheme)
 - [Django default auth](https://docs.djangoproject.com/en/3.2/topics/auth/default/)
 - [Expose vs publish Docker](https://www.baeldung.com/ops/docker/expose-vs-publish)
 - [Django Pagination](https://docs.djangoproject.com/en/3.2/topics/pagination/)
 - [django-taggit](https://django-taggit.readthedocs.io/en/latest/api.html)

# Problemas conocidos / posibles mejoras

 - No hay prevención de subtareas circulares
 - La búsqueda por titulo es exacta cuando podría ser más elástica
   - Posible solución: Incorporar como tags e ignorando stop-words
