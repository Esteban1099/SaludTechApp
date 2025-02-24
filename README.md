# Entrega Semana 5

A continuación presentamos la entrega de la semana cinco.

En esta entrega presentamos un microservicio con comunicacion asincrona (comandos y eventos) usando Apache Pulsar.

NO se espera tener el servicio completamente desarrollado, solo los comandos, consultas e infraestructura necesaria (tablas, repositorios, etc) para satisfacer los futuros escenarios de calidad (implemente lo necesario para eventualmente probarlo en la siguiente entrega).

# Instruccion de ejecucion del proyecto

1. Clonar el repositorio
2. Crear imagenes Docker para sta y notificaciones
```bash
docker build -f sta.Dockerfile -t sta .
```
```bash
docker build -f notificaciones.Dockerfile -t notificaciones .
```
3. Ejecutar el siguiente comando para desplegar toda la arquitectura
```bash
docker compose up -d
```
4. Una vez los proyectos terminen de subir puede ejecutar la coleccion de postman adjunta en el proyecto y ver su funcionamiento
![img.png](img.png)
