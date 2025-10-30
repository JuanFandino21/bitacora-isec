**Bitácora ISec – App Multicontenedor (Docker Compose)**

Bitácora ISec es una libretica en la web para anotar cosas que haces o encuentras de infraestructura y seguridad computacional. Sirve para registrar y priorizar lo que se hace o se encuentra para la asignatura, mientras se demuestra la arquitectura multicontenedor.
Priorizar automáticamente lo importante: el worker marca severidad (baja/medio/alta) según lo que escribes (ej: “credenciales por defecto” es alta).


**Integrantes del grupo**

Alejandro Arana Fernández – 2220232039
Anthony Sebastian Vanegas Aguirre – 2220251055
Juan David Fandiño Hernández – 2220221087
Nicolle Alexandra Bustos Penagos – 2220231022
Yaiza Angelina Sánchez Dueñez – 2220232034

**Objetivos del proyecto**

Objetivo general. Definir y ejecutar una aplicación docker multicontenedor usando Docker Compose (y ejecutada en plataforma Linux).

Objetivo específico. Mostrar la secuencia de configuración del archivo docker-compose.yml que permita crear servicios, enlaces entre servicios, volúmenes, habilitar puertos y crear redes. Además, publicar las imágenes en Docker Hub y explicar el proceso en video.

Arquitectura 

backend (Python/Flask): API CRUD /api/registros con Postgres; cachea listados en Redis.
worker (Python): lee la cola cola:clasificar en Redis y ajusta severidad (baja, media, alta) por reglas simples en español.
web (Node/Express): página limpia sin frameworks pesados; crea y lista registros.
db (PostgreSQL): persistencia.
redis (Redis): caché y cola.
compose (Docker Compose): define servicios, enlaces por nombre, volúmenes, puertos y red appnet.

