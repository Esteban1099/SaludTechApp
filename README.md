# Entrega Semana 5

A continuación presentamos la entrega de la semana cinco.

En esta entrega presentamos un microservicio con comunicacion asincrona (comandos y eventos) usando Apache Pulsar.

NO se espera tener el servicio completamente desarrollado, solo los comandos, consultas e infraestructura necesaria (tablas, repositorios, etc) para satisfacer los futuros escenarios de calidad (implemente lo necesario para eventualmente probarlo en la siguiente entrega).

# Instruccion de ejecucion del proyecto

1. Clonar el repositorio
2. Crear imagenes Docker para ingesta automatizada, sta3, notificaciones, canonizacion y bff
```bash
docker build -f ingesta_automatizada.Dockerfile -t ingesta_automatizada .
```
```bash
docker build -f sta3.Dockerfile -t sta3 .
```
```bash
docker build -f notificaciones.Dockerfile -t notificaciones .
```
```bash
 docker build -f canonizacion.Dockerfile -t canonizacion .
```
```bash
docker build -f bff.Dockerfile -t bff .
```
3. Ejecutar el siguiente comando para desplegar toda la arquitectura
```bash
docker compose up -d
```
4. Una vez los proyectos terminen de subir puede ejecutar la coleccion de postman adjunta en el proyecto y ver su funcionamiento
![img.png](img.png)

# Escenarios de calidad

## 1. Soportar un aumento de centros de salud conectados
A medida que SaludTech expande sus operaciones a lo largo del continente americano, se agregan cientos de nuevos centros de salud a la plataforma, aumentando el volumen de datos procesados. El sistema debe escalar para poder procesar esto datos sin afectar el rendimiento.
![image](https://github.com/user-attachments/assets/744cfcc8-923c-414c-8444-64c70441b84e)

## 2. Protección de datos anonimizados
Como parte del cumplimiento con regulaciones como HIPAA, los datos deben almacenarse y transmitirse de manera segura para evitar exposición de información sensible.
![image](https://github.com/user-attachments/assets/21554302-c34b-423a-9910-2f3aca2ad0a2)

## 3. Monitoreo proactivo de la infraestructura
Implementar monitoreo en tiempo real para prevenir fallos antes de que afecten a los usuarios.
![image](https://github.com/user-attachments/assets/515b6fe6-8cf4-4f18-bf1a-8f544e2b86fa)

# División de trabajo

1. BFF - Johanna Beltrán
2. Ingesta automatizada (STA) y notificación - Alejandro Martinez
3. Canonización - Fernando Garzón
4. Procesamiento imagen (STA3) - Esteban Reyes

# Video Semana 6
[Entrega semana 6](https://drive.google.com/file/d/1M952Uk35ohT4_VIlSeWzb7hRNUSRGCMn/view?usp=drive_link)









