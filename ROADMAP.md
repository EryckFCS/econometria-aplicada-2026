# 🗺️ Roadmap: Ecosistema de Econometría Aplicada 2026

Este documento detalla los objetivos, el progreso y la arquitectura del sistema de automatización para la cátedra de Econometría Aplicada.

## 🎯 Visión General
Eliminar el procesamiento manual de datos y la elaboración manual de reportes mediante una canalización (pipeline) que integra APIs internacionales, scrapers locales y auditoría forense de datos.

---

## 🛠️ Estado del Proyecto

### Fase 1: Cimientos y Auditoría Forense 🟢 (Completado)
*   **Infraestructura de Datos**: Implementación de una arquitectura de capas (`data/`, `src/`, `docs/`, `stata/`).
*   **Motor Forense**: Sistema de auditoría que genera métricas de integridad y trazabilidad para cada observación descargada.
*   **Conector World Bank**: Integración robusta vía API de los Indicadores de Desarrollo Mundial (WDI).
*   **Buscador Terminado**: Prototipo funcional de `wb_search.py` para discovery de variables.
*   **Empaquetador EVA**: Script `zip_task.py` para generar entregables universitarios con un solo comando.

### Fase 2: Macro-Global y Mercados 🟡 (En curso)
*   **High-Frequency Data**: Scraper de mercados (Petróleo, Metales, Índices) vía `yfinance` operativo.
*   **Universal Macro Lake**: Descarga e integración de la base masiva del FMI (World Economic Outlook).
*   **Historical Context**: Integración del Maddison Project Database (PIB histórico).
*   **Próximo Pasito**: Consolidar el cargador (`Harmonizer`) que une fuentes discrepantes en un panel balanceado.

### Fase 3: Local Forensics (Ecuador) 🔴 (Pendiente)
*   **BCE Integration**: Scraper automatizado para Cuentas Nacionales del Banco Central del Ecuador.
*   **INEC Secure Bridge**: Automatización de descargas de microdatos ENEDMU / IPC (Requiere gestión de credenciales).
*   **Agregador Temporal**: Lógica para convertir datos diarios/mensuales a frecuencias anuales/trimestrales sin perder precisión estadística.

### Fase 4: Orquestación Académica ⚪ (Próximamente)
*   **Stata Automation**: Puente dinámico para que los archivos `.do` consuman directamente el Data Lake procesado.
*   **Auto-Reporting**: Generación de tablas de regresión automáticas en Word/LaTeX con formato APA/Econometrica.
*   **Auditoría de Replicabilidad**: Script que verifica que cualquier tercero pueda recrear los resultados desde cero con un solo comando (`make all` o `python main.py`).

---

## 📐 Doctrina de Datos
1.  **Prioridad API**: Si existe una API estable, no se descarga el archivo completo (ej. World Bank).
2.  **Descarga Crítica**: Se descarga el set de datos completo solo si no hay API o si la trazabilidad forense lo exige (ej. IMF, Maddison).
3.  **Cero Manualidad**: Se prohíbe el "Copy-Paste" de datos. Todo movimiento de datos debe ser scriptado y logueado por `structlog`.

---
*Última actualización: 12 de abril de 2026*
