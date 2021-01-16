# dear_diary
dear_diary pretende ser un diario digital en formato de aplicación web, el cual permita a sus distintos usuarios
recopilar lo que les pasa día a día y que estos puedan puntuar sus estados o "moods"

## Estado
```diff
+ [En desarrollo]
```

## Cómo funciona la configuración
Se ha hecho uso del módulo [django-environ](https://django-environ.readthedocs.io/en/latest/)

Este módulo, permite definir a partir de variables de entorno distintas configuraciones para
distintos entornos, a partir de un fichero .env

En concreto, se debe crear un fichero .env en el directorio dear_diary, con las siguientes
variables de entorno:
- SECRET_KEY=[SECRET_KEY]
- DEBUG=[True|False]
- ALLOWED_HOSTS=[ALLOWED_HOST1,...,ALLOWED_HOSTN]
- SQLITE_URL=[sqlite:///full/path/to/sqlite/database]
- STATIC_ROOT=[full/path/to/static/]
- MEDIA_ROOT=[full/path/to/media]

## Planificación
- [:white_check_mark:] v0.1.0 -> estructura básica del proyecto
- [:white_check_mark:] v0.2.0 -> landing page y página de registro
![v0.2.0_landing](screenshots/v0.2.0_landing.png)
![v0.2.0_singup](screenshots/v0.2.0_singup.png)
- [:white_check_mark:] v0.3.0 -> modelo de mood y dashborad de moods
![v0.3.0](screenshots/v0.3.0.png)
- [:white_check_mark:] v0.4.0 -> CRUD de moods y logout
![v0.4.0_dashboard](screenshots/v0.4.0_dashboard.png)
![v0.4.0_new](screenshots/v0.4.0_new.png)
![v0.4.0_edit](screenshots/v0.4.0_edit.png)
- [:white_check_mark:] v0.5.0 -> perfil del usuario
![v0.5.0_profile](screenshots/v0.5.0_profile.png)
![v0.5.0_edit_profile](screenshots/v0.5.0_edit_profile.png)
- [] v0.6.0 -> setup de producción

