## Comparativa: PostgreSQL Estándar vs. PostgreSQL en Supabase

| Característica | PostgreSQL Estándar (Tradicional/Autohospedado) | PostgreSQL en Supabase |
| :--- | :--- | :--- |
| **Concepto de *Proyecto*** | La base de datos se gestiona como una **instancia única** (ej. un servidor o *cluster*). Cada aplicación o microservicio puede usar una **base de datos separada** o esquemas dentro de la misma instancia. | La base de datos es el **corazón del Proyecto Supabase**. Un proyecto incluye la instancia de Postgres *junto con* servicios integrados (Auth, Storage, Functions, Realtime). |
| **Integración de Servicios** | Requiere que el desarrollador configure y conecte manualmente servicios externos para autenticación, APIs y almacenamiento de archivos (ej. Redis, Express.js, S3). | **Integración *Out-of-the-Box***. Los servicios (Auth, Storage, Realtime) están preconfigurados para interactuar directamente con la base de datos a través de **extensiones** o *proxies* (PostgREST, GoTrue). |
| **Exposición de API** | Requiere un servidor intermedio (ej. Node.js/Python) para escribir la lógica de API, validar y exponer *endpoints* REST/GraphQL a los clientes. | **API Instantánea Automática**. Utiliza la extensión **PostgREST** (un servidor *proxy* de Go) para generar automáticamente *endpoints* RESTful funcionales y seguros basados en el esquema de tu base de datos. |
| **Esquema `public`** | El esquema `public` se usa comúnmente, pero a menudo se recomienda usar **esquemas personalizados** para la organización lógica y aislamiento de las aplicaciones. | **Foco en el Esquema `public`**. Supabase te **"empuja" a usar** y a centrar tu estructura de datos en el esquema `public`, ya que es el esquema principal que el **API Instantánea** y las herramientas de Supabase observan y exponen por defecto. |
| **Seguridad de Datos** | Se implementa mediante **permisos de usuario y roles tradicionales** a nivel de la base de datos o mediante lógica de validación en el servidor de aplicación (backend). | Se basa principalmente en **Políticas de Seguridad a Nivel de Fila (RLS)**. El servicio de Autenticación integra el **JWT** directamente con las funciones de RLS de Postgres para un control de acceso granular. |
| **Gestión de Sesiones/Roles**| La aplicación gestiona la sesión de usuario y las credenciales de la base de datos (pool de conexiones). | La gestión de sesión se maneja mediante el **JWT** y el servicio **Auth** de Supabase. El token es interpretado por Postgres para establecer roles y `auth.uid()` para las políticas RLS. |
| **Extensiones** | Se pueden instalar la mayoría de las extensiones disponibles, pero la configuración y el mantenimiento son manuales. | Incluye un conjunto de **extensiones clave preinstaladas** y gestionadas (como `pg_graphql`, `uuid-ossp`, etc.) que son necesarias para el funcionamiento de los servicios de Supabase. |

---

## Conclusión del Modelo Supabase

El PostgreSQL de Supabase no es solo una base de datos, sino un **servidor de aplicaciones integrado**. Se encarga de:

1.  **Exponer la API** sin escribir código de servidor (gracias a PostgREST).
2.  **Manejar la seguridad** a nivel de base de datos (gracias a RLS).
3.  **Proporcionar la funcionalidad de tiempo real** (gracias al servicio Realtime).

Esto permite a los desarrolladores centrarse casi exclusivamente en la lógica de su base de datos y en su aplicación *frontend*, eliminando la necesidad de escribir y mantener la capa de API tradicional.

