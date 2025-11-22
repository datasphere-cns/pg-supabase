# Supabase

**Supabase** es una plataforma de desarrollo que se presenta como una alternativa a **Firebase** de Google. Su objetivo principal es simplificar la creación de *backends* escalables para tus aplicaciones, proporcionando una suite completa de herramientas esenciales para el desarrollo *web* y móvil.

La filosofía de Supabase es utilizar y extender tecnologías probadas y maduras, siendo la base de datos **PostgreSQL** su núcleo fundamental. 

## Servicios Clave de Supabase

Supabase ofrece varios servicios integrados que trabajan conjuntamente para proporcionar una experiencia completa de *backend* como servicio (BaaS).

### 1. Base de Datos (PostgreSQL)

El corazón de Supabase es una base de datos **PostgreSQL** totalmente gestionada.

* **Rendimiento y Fiabilidad:** PostgreSQL es reconocido por su robustez, características avanzadas (como JSONB, PostGIS) y cumplimiento estricto de estándares.
* **Extensiones:** Soporta una gran cantidad de **extensiones de PostgreSQL**, lo que permite añadir funcionalidades como búsquedas de texto completo, manejo geoespacial y más.
* **Acceso Directo:** A diferencia de otras soluciones BaaS, tienes **acceso completo** a la base de datos.

### 2. Autenticación (*Auth*)

Proporciona un servicio de autenticación listo para usar que maneja la gestión de usuarios.

* **Métodos Versátiles:** Soporta el registro por correo electrónico y contraseña, inicio de sesión con redes sociales (OAuth), *Magic Links*, y autenticación de un solo uso (OTP).
* **Seguridad:** Utiliza **JSON Web Tokens (JWT)** para gestionar las sesiones de forma segura.
* **Gestión de Usuarios:** Incluye funcionalidades para restablecimiento de contraseñas y verificación de correo electrónico.

### 3. API Instantánea (*Realtime*)

Este es uno de los servicios más potentes, ya que genera automáticamente APIs a partir de tu esquema de PostgreSQL.

* **APIs RESTful y GraphQL:** Se generan automáticamente **endpoints RESTful** y, opcionalmente, de **GraphQL** que te permiten interactuar con tus tablas de forma segura.
* **Tiempo Real:** El servicio **Realtime** permite a las aplicaciones escuchar los **cambios de la base de datos** (inserciones, actualizaciones, eliminaciones) a través de *WebSockets*, lo que es crucial para la construcción de experiencias en tiempo real (como chats o notificaciones en vivo).

### 4. Almacenamiento (*Storage*)

Un servicio de gestión de archivos escalable para almacenar objetos grandes (como imágenes, videos, documentos, etc.).

* **Buckets y Archivos:** Organiza los archivos en *buckets* (cubos), similar a S3 de AWS.
* **Reglas de Seguridad:** La seguridad del almacenamiento se gestiona a través de las **Políticas de Seguridad a Nivel de Fila (RLS)** de PostgreSQL, lo que proporciona un control de acceso granular y unificado.

### 5. Funciones *Edge* (*Edge Functions*)

Permite ejecutar código sin servidor (*serverless*) escrito en **TypeScript** o **JavaScript** utilizando la tecnología **Deno**.

* **Baja Latencia:** Se ejecutan cerca del usuario (*Edge*), lo que minimiza la latencia.
* **Casos de Uso:** Ideales para *webhooks*, tareas en segundo plano o la lógica de negocio que no es adecuada para ejecutarse directamente en la base de datos.

---

## En Resumen

Supabase ofrece una solución **unificada** donde la base de datos PostgreSQL no solo almacena tus datos, sino que también sirve como el **punto central de seguridad** y la **fuente de las APIs** de tus aplicaciones, simplificando significativamente la arquitectura de tu *backend*.

## 👤 Autor

* **Nombre:** Nelson Zepeda
* **Correo Electrónico:** nelson.zepeda@datasphere.tech
* **LinkedIn:** [Nelson Zepeda](https://www.linkedin.com/in/nelsonzepeda733/)
* **Fecha de Documentación:** Noviembre 2025
