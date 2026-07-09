---
name: Stata Batch Execution Protocol
description: Protocolo para la ejecución por lotes sin interfaz gráfica (headless) de scripts de Stata (.do) utilizando Wine en Linux con trazabilidad de logs y gestión de dependencias.
---

# Stata Batch Execution Protocol

Este protocolo define las directrices y procedimientos que debe seguir el agente para ejecutar scripts de Stata (`.do`) de manera no interactiva (headless) en el entorno Linux utilizando Wine, garantizando trazabilidad total de logs y control de errores.

## 1. Configuración Obligatoria del Script (.do)

Todo archivo de Stata (`.do`) que sea ejecutado o creado bajo este protocolo debe contar con la siguiente configuración inicial obligatoria para evitar interrupciones en la terminal y asegurar consistencia:

```stata
*==============================================================================*
* CONFIGURACIÓN INICIAL OBLIGATORIA
*==============================================================================*
clear all
macro drop _all
set more off
set graphics off
set seed 42
```

- **`clear all` & `macro drop _all`**: Limpieza completa de memoria y variables globales.
- **`set more off`**: Evita pausas por paginación en la consola de salida.
- **`set graphics off`**: Desactiva la renderización interactiva de ventanas de gráficos para prevenir bloqueos en entornos headless.
- **`set seed 42`**: Garantiza la reproducibilidad estocástica de estimaciones y simulaciones.

---

## 2. Gestión de Dependencias y Paquetes en Stata

Para evitar errores por falta de paquetes de la comunidad (SSC) sin reinstalar innecesariamente:
- Se debe validar la instalación previa utilizando la estructura `capture ssc install`.
- Ejemplo de carga limpia de paquetes:
```stata
capture ssc install collin
capture ssc install estout
capture ssc install wbopendata
```

---

## 3. Comando de Ejecución Headless vía Wine

La ejecución debe realizarse apuntando al ejecutable de Stata SE configurado en el sistema a través de Wine con el flag `/e` (que fuerza el modo batch headless y salida limpia):

```bash
wine /home/erick-fcs/.local/share/Stata18/StataSE-64.exe /e do <ruta_al_script.do>
```

> [!IMPORTANT]
> El comando debe ejecutarse en segundo plano o con un tiempo de espera controlado, estableciendo el directorio de trabajo (`Cwd`) en la carpeta del script respectivo para evitar fallos de resolución de rutas relativas.

---

## 4. Trazabilidad de Logs y Criterio de Éxito

La ejecución se considera **exitosa** únicamente si se cumplen estas dos condiciones:
1. El comando de terminal retorna un código de salida `0`.
2. Se genera y verifica el archivo de log correspondiente (ej. `.log` o `.txt` especificado en el comando `log using`) sin registrar errores fatales o interrupciones en las últimas líneas del archivo.

El agente **debe leer y analizar** el log resultante utilizando la herramienta `view_file` para extraer los coeficientes econométricos, test estadísticos e integridades descriptivas y presentárselos estructuradamente al usuario.

---

## 5. Protocolo de Escalación ante Fallos

Si la ejecución falla o se bloquea:
1. **Error de Paquetes/Dependencias:** Si el log indica fallos en la conexión o en la instalación automática de un comando SSC, el agente debe detenerse inmediatamente y solicitar asistencia humana a Erick para la verificación o instalación manual de dichos recursos.
2. **Código de Salida no Cero:** Si Wine o Stata retornan un error de ejecución, el agente debe reportar el estado de bloqueo (`BLOCKED`) mostrando las últimas líneas del log de salida donde se originó el error de sintaxis o estimación.
