# Aspectos Esenciales a Considerar en Supabase

Al trabajar con Supabase, hay varios detalles de configuración y seguridad que impactan directamente en el desarrollo y despliegue de la aplicación.

## 1. El Problema de la Conectividad IP: La Limitación de IPv6

Supabase opera con una arquitectura moderna que prioriza el direccionamiento **IPv6** por defecto. Si bien esto es técnicamente avanzado, se convierte en una **restricción** para la mayoría de los escenarios de desarrollo y producción actuales.

### El Impacto Directo en el Desarrollo

| Problema de Conectividad | Impacto Operacional | Solución (Costo) |
| :--- | :--- | :--- |
| **Dependencia IPv6** | La base de datos es inalcanzable para cualquier servicio o herramienta que **no soporte IPv6** (muchas herramientas de monitoreo, *VPNs* corporativas, o servicios *legacy*). | **Pago Adicional.** Se debe habilitar manualmente la dirección IPv4 estática en la configuración del proyecto, incurriendo en un **costo mensual recurrente**. |
| **Integración con *Webhooks*** | Si un servicio externo (como un sistema de pago o un proveedor de SMS) necesita hacer un *callback* a tu base de datos de Supabase, a menudo fallará si solo utiliza IPv4. | **Pago Adicional.** La única solución para garantizar el acceso desde el ecosistema IPv4 es **pagar y habilitar IPv4 estática**. |
| **Herramientas de Administración** | Algunas herramientas de gestión de bases de datos o *scripts* de *deployment* fallan al resolver o conectarse a una dirección IPv6. | La única alternativa sin pagar es configurar *proxies* o *tunnels* complejos que traduzcan la conexión, añadiendo **fricción y complejidad**. |

> **Conclusión para el Desarrollador:** La elección de IPv6 por defecto fuerza al desarrollador a **pagar por un recurso (IPv4)** que es esencial para la compatibilidad con la infraestructura de Internet actual. En la práctica, si necesitas conectividad de red estándar y fiable, la **habilitación de IPv4 es un requisito funcional** y no una opción.
---

## 2. Gestión de Claves de Conexión

Supabase utiliza tres tipos de claves **JWT** para gestionar los permisos de acceso a sus APIs (PostgREST, Auth, Storage). Todas las claves se encuentran en la sección "API Settings".

| Nombre de la Clave | Propósito y Uso | Nivel de Permiso | Seguridad |
| :--- | :--- | :--- | :--- |
| **`anon` Key (Clave Anónima)** | Diseñada para el **uso público en el *frontend*** de tu aplicación. Se utiliza para acceder a funciones y datos antes de que el usuario haya iniciado sesión (ej. leer una lista de productos). | Acceso limitado. Solo puede realizar acciones permitidas por las políticas **RLS** para el rol `anon` (usuario no autenticado). | **Baja Seguridad.** Debe ser incluida en el código del *frontend*. Depende de RLS para la seguridad. |
| **`service_role` Key (Clave de Rol de Servicio)** | Diseñada para **operaciones de *backend* o servidores de confianza** (Ej. Edge Functions, un servidor Node.js privado, *scripts* de migración). | **Máximo Acceso.** **Bypassea (ignora)** todas las Políticas de Seguridad a Nivel de Fila (RLS). Tiene permisos de superusuario. | **Alta Seguridad.** **Nunca debe exponerse al lado del cliente (frontend)**. Su uso implica total responsabilidad del desarrollador sobre la lógica de seguridad. |
| **JWT *Secret*** | No es una clave de conexión directa. Es el **secreto criptográfico** que usa Supabase para firmar (crear) y verificar la autenticidad de todos los **Tokens Web JSON (JWTs)**. | N/A | **Crítica.** Se utiliza para validar tokens en servicios externos (ej. Edge Functions). **Nunca debe ser expuesta.** |

---

## 3. Uso de Esquemas de Base de Datos

Por defecto, Supabase expone el esquema **`public`** a través de sus APIs instantáneas (PostgREST/Realtime).

### Implicación de Usar Esquemas Diferentes a `public`
Utilizar un esquema diferente a `public` (ej. `app_data`, `billing`) tiene las siguientes implicaciones:

* **Aislamiento de Lógica Privada:** Es la **práctica recomendada** para almacenar tablas y funciones sensibles o internas (ej. secretos de API, datos de facturación, lógica de *webhooks*).
* **Protección por Defecto:** Las tablas en esquemas que no son `public` **no son accesibles** por la API instantánea generada automáticamente, ni por el servicio Realtime. Esto proporciona una capa de seguridad y aislamiento por diseño.

> **Recomendación:** Todo lo que el cliente final (frontend) necesita ver o manipular, debe estar en el esquema **`public`** y tener **RLS activado**. Todo lo que es interno puede estar en un **esquema privado**.

---

## 4. El "Dolor" del RLS (Row-Level Security)

RLS es la columna vertebral de la seguridad en Supabase, pero a menudo es la fuente de frustración para los nuevos usuarios.

### El Desafío Principal
El error más común es olvidar que **RLS está desactivado por defecto** para las nuevas tablas.

> Si RLS está desactivado, **TODOS** los usuarios (incluidos los anónimos) pueden leer y escribir en la tabla usando el `anon` key.

### Dolor Común y Solución
| Dolor (Problema) | Causa Raíz | Solución en Supabase |
| :--- | :--- | :--- |
| **"Mi *frontend* no puede obtener datos."** | **RLS está activado** en la tabla, pero **NO existe ninguna política** para la operación solicitada (`SELECT`). | Crea una política RLS de tipo `SELECT` que permita el acceso al usuario. |
| **"No puedo insertar/actualizar datos."** | **RLS está activado**, pero **NO existe una política** de tipo `INSERT` o `UPDATE`. | Crea una política RLS que permita las acciones (`INSERT`/`UPDATE`) basándose en la identidad del usuario (`auth.uid()`). |
| **"Funciona con la *service_role* key, pero no con la *anon* key."** | La **`service_role` key bypassea RLS**, probando que el problema es de la **política RLS** (o su ausencia), no de la conexión o la consulta. | Revisa y corrige la lógica de las políticas RLS. Asegúrate de que la política esté configurada para el rol correcto (`anon` o `authenticated`). |



### 💡 Consejo
El **Supabase Studio** (la interfaz web) te permite crear y probar tus políticas RLS fácilmente antes de moverte al código.
