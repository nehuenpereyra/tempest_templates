# Grupo 20

## Integrantes

Iyael Lihue Pereyra - 16440/6

Nehuen Pereyra - 15926/1

---

## Información de Acceso

### Usuario Administrador

Correo: admin@admin.com

Pass: admin123

---

## Defición de API

### Centros de Ayuda

_Aclaraciones:
El archivo que contiene el codigo correspondiente a la api de centros de ayuda se encuentra en `app/resources/api/help_center.py`._

_Se utilizo para su desarrollo Flask nativo y Flask-WTF (para realizar las validaciones)._

_No se realizó ningun cambio adicional en el modelo._

### Listar

**Ruta:** `/api/centros`

**Metodo:** `GET`

**Argumentos:**

- `pagina`

**Codigos de error:**

- 400 Bad Request (pagina < 1)

**Ejemplo exitoso:**

```json
{
  "centros": [
    {
      "direccion": "Av 80 e20 y 21 nro 90",
      "email": "papa@centro.org",
      "hora_apertura": "09:00",
      "hora_cierre": "16:00",
      "nombre": "Centro la Papa",
      "telefono": "+54 294 410-2030",
      "tipo": "Centro de Alimentos",
      "web": "https://papa.centro.org"
    }
  ],
  "pagina": 1,
  "por_pagina": 4,
  "total": 1
}
```

### Ver

**Ruta:** `/api/centro/<int:id>`

**Metodo:** `GET`

**Argumentos:**

- N/A

**Codigos de error:**

- 404 Not Found

**Ejemplo exitoso:**

```json
{
  "atributos": {
    "direccion": "Av 80 e20 y 21 nro 90",
    "email": "papa@centro.org",
    "hora_apertura": "09:00",
    "hora_cierre": "16:00",
    "nombre": "Centro la Papa",
    "telefono": "+54 294 410-2030",
    "tipo": "Centro de Alimentos",
    "web": "https://papa.centro.org"
  }
}
```

### Crear

**Ruta:** `/api/centro`

**Metodo:** `POST`

**Argumentos:**

- `nombre*`
- `direccion*`
- `telefono*`
- `hora_apertura*`
- `hora_cierre*`
- `tipo*`
- `municipio*`
- `web_url`
- `email`
- `latitud`
- `longitud`

**Codigos de error:**

- 400 Bad Request

**Ejemplo sin campos opcionales:**

Cuerpo de la solicitud

```json
{
  "nombre": "Centro Vikingo",
  "direccion": "Calle 90",
  "telefono": "+54 2944 208060",
  "hora_apertura": "09:30",
  "hora_cierre": "10:00",
  "tipo": "Centro de Sangre",
  "municipio": "Avellaneda"
}
```

Cuerpo de la respuesta

```json
{
  "atributos": {
    "direccion": "Calle 90",
    "hora_apertura": "09:30",
    "hora_cierre": "10:00",
    "municipio": "Avellaneda",
    "nombre": "Centro Vikingo",
    "telefono": "+54 2944 208060",
    "tipo": "Centro de Sangre"
  }
}
```

**Ejemplo con campos opcionales:**

Cuerpo de la solicitud

```json
{
  "nombre": "Centro Vikingo",
  "direccion": "Calle 90",
  "telefono": "+54 2944 208060",
  "hora_apertura": "09:30",
  "hora_cierre": "10:00",
  "tipo": "Centro de Sangre",
  "municipio": "Avellaneda",
  "web_url": "https://vikingo.centro.org",
  "email": "ragnar@midgard.org",
  "latitud": -20.125543,
  "longitud": 10.204012
}
```

Cuerpo de la respuesta

```json
{
  "atributos": {
    "direccion": "Calle 90",
    "email": "ragnar@midgard.org",
    "hora_apertura": "09:30",
    "hora_cierre": "10:00",
    "latitud": -20.125543,
    "longitud": 10.204012,
    "municipio": "Avellaneda",
    "nombre": "Centro Vikingo",
    "telefono": "+54 2944 208060",
    "tipo": "Centro de Sangre",
    "web_url": "https://vikingo.centro.org"
  }
}
```

**obs:** En la base de datos se cargaron 3 tipos de centro de ayuda:

- `Centro de Alimentos`
- `Centro de Ropa`
- `Centro de Sangre`

### Turno

_Aclaraciones:
El archivo que contiene el codigo correspondiente a la api de turno se encuentra en `app/resources/turn.py`._

_Se utilizo para su desarrollo Flask nativo y Flask-WTF (para realizar las validaciones)._

_En el modelo se agrego un metodo llamado `all_free_time_json` el cual retorna un json con los turnos libres._

### Ver turnos disponibles para una fecha

**Ruta:** `/api/centros/<int:id>/turnos_disponibles/?fecha=<date:día-mes-año>`

**Metodo:** `GET`

**Argumentos:**

- `fecha (formato: dia-mes-año)`

**Codigos de error:**

- 400 Bad Request (fecha con formato invalido)

**Ejemplo exitoso:**

```json
{
  "turnos": [
    {
      "centro_id": "2",
      "horario_inicio": "09:00",
      "horario_fin": "09:30",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "09:30",
      "horario_fin": "10:00",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "10:00",
      "horario_fin": "10:30",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "10:30",
      "horario_fin": "11:00",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "11:00",
      "horario_fin": "11:30",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "11:30",
      "horario_fin": "12:00",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "12:00",
      "horario_fin": "12:30",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "12:30",
      "horario_fin": "13:00",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "13:00",
      "horario_fin": "13:30",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "13:30",
      "horario_fin": "14:00",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "14:00",
      "horario_fin": "14:30",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "14:30",
      "horario_fin": "15:00",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "15:00",
      "horario_fin": "15:30",
      "fecha": "2020/11/15"
    },
    {
      "centro_id": "2",
      "horario_inicio": "15:30",
      "horario_fin": "16:00",
      "fecha": "2020/11/15"
    }
  ],
  "centro": "Centro la Papa"
}
```

### Solicitar reserva de un turno

**Ruta:** `/api/centros/<int:id>/reserva`

**Metodo:** `POST`

**Argumentos:**

- `centro_id*`
- `email_donante*`
- `telefono_donante`
- `hora_inicio*`
- `hora_fin*`
- `fecha*`

**Codigos de error:**

- 400 Bad Request

**Ejemplo:**

Cuerpo de la solicitud

```json
{
  "centro_id": 2,
  "email_donante": "juan.perez@gmail.com",
  "telefono_donante": "221 - 5930941",
  "hora_inicio": "11:00",
  "hora_fin": "11:30",
  "fecha": "2020-11-13"
}
```

Cuerpo de la respuesta

```json
{
  "atributos": {
    "centro_id": 2,
    "email_donante": "juan.perez@gmail.com",
    "fecha": "2020-11-13",
    "hora_fin": "11:30",
    "hora_inicio": "11:00",
    "telefono_donante": "221 - 5930941"
  }
}
```
