# 🗺️ Roadmap: Ecosistema de Econometría Aplicada 2026

Este documento detalla los objetivos, el progreso y la arquitectura del sistema de automatización para la cátedra de Econometría Aplicada.

## 🎯 Visión General

Eliminar el procesamiento manual de datos y la elaboración manual de reportes mediante una canalización (pipeline) que integra APIs internacionales, scrapers locales y auditoría forense de datos.

---

## 🛠️ Estado del Proyecto

### Fase 1: Cimientos y Auditoría Forense 🟢 (Completado)

- **Infraestructura de Datos**: Arquitectura de capas (`src/core/`, `src/lib/`, `src/tasks/`, `config/`, `data/`).
- **Motor Modular**: Desacoplamiento de perfiles, backends, motor y exportadores.
- **Diccionario Automatizado**: Generación de metadatos en Excel Maestro.
- **Empaquetado reproducible**: Orquestadores directos bajo `src/tasks/` con perfiles declarativos y backends intercambiables.

### Fase 2: Macro-Global y Mercados 🟡 (En curso)

- **High-Frequency Data**: Scraper de mercados (Petróleo, Metales, Índices) vía `yfinance` operativo.
- **Universal Macro Lake**: Descarga e integración de la base masiva del FMI (World Economic Outlook).
- **Historical Context**: Integración del Maddison Project Database (PIB histórico).
- **Próximo Pasito**: Consolidar el cargador que une fuentes discrepantes en un panel balanceado.

### Fase 3: Local Forensics (Ecuador) 🔴 (Pendiente)

- **BCE Integration**: Scraper automatizado para Cuentas Nacionales del Banco Central del Ecuador.
- **INEC Secure Bridge**: Automatización de descargas de microdatos ENEMDU / IPC (requiere gestión de credenciales).
- **Agregador Temporal**: Lógica para convertir datos diarios y mensuales a frecuencias anuales o trimestrales sin perder precisión estadística.

### Fase 4: Orquestación Académica 🟡 (En curso)

- **Task Orchestrators**: Independencia total de scripts (ACD, AA, APE) mediante inyección de librerías.
- **Syllabus Sync**: Documentación técnica automática por unidad.
- **Governance Hub**: Repositorio de manuales y validación de metadatos (CI-Catalog).
- **Stata Automation**: Puente dinámico para archivos `.do`.

### Fase 5: Inteligencia y Publicación 🔴 (Pendiente)

- **Paper Engine (End-to-End)**: Motor que genera borradores automáticos en Word/LaTeX dignos de publicación (Estructura IMRyD + Tablas APA).
- **Bibliography Governance**: Sistema similar al catálogo pero para referencias bibliográficas y fuentes de inteligencia (WSJ/RAG).
- **Self-Healing Engine**: Sistema de auto-curación que detecta fallos en APIs y busca automáticamente proxies o métodos alternos.
- **Docker Health Monitor**: Contenedores para monitorizar la salud del Data Lake y los procesos de ingesta.

---

## 📐 Doctrina de Datos

1. **Prioridad API**: Si existe una API estable, no se descarga el archivo completo (ej. World Bank).
2. **Descarga Crítica**: Se descarga el set de datos completo solo si no hay API o si la trazabilidad forense lo exige (ej. IMF, Maddison).
3. **Cero Manualidad**: Se prohíbe el "Copy-Paste" de datos. Todo movimiento de datos debe ser scriptado y logueado por `structlog`.

---

Última actualización: 14 de abril de 2026 (perfil declarativo + backends genéricos).
