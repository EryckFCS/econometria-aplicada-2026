---
# WORKFLOW: Ingesta de Datos al Exocórtex RAG
- Descripción: Ingesta estandarizada y soberana de PDFs de investigación, reportes SBS, boletines y literatura económica al vault de conocimiento utilizando el servidor MCP `capital-rag`.
- **Versión**: 2.0.0
---

## 1. Cuándo Invocar este Workflow

Debe utilizarse al adquirir nuevos documentos académicos (`.pdf`, `.md`, `.txt`) o regulatorios que requieran enriquecer la memoria de largo plazo de las colecciones activas del ecosistema.

---

## 2. Prerrequisitos

- Servidor MCP `capital-rag` activo y registrado en el entorno de desarrollo.
- Archivo de origen (`.pdf`, `.md`, `.txt`) disponible en una ruta absoluta local (ej. en `temp_readings/raw/` o dentro de la estructura de los repositorios activos).

---

## 3. Pasos del Proceso y Herramientas Activas

### Paso 1: Verificar el Estado de Cobertura y Salud del Vault
Antes de la ingesta, podemos inspeccionar las estadísticas del exocórtex y la cobertura temática.
- **Herramienta**: `capital-rag:rag_dashboard`
- **Uso**: Ejecutar la herramienta sin parámetros para obtener el resumen de salud.

### Paso 2: Ingesta Soberana Automatizada
Indexar el documento directamente en la colección correspondiente (por defecto `global_knowledge`).
- **Herramienta**: `capital-rag:rag_ingest_file`
- **Parámetros**:
  - `file_path`: Ruta absoluta del archivo local a ingestar (ej. `/home/erick-fcs/Capital_Workstation/capital-workstation-libs/temp_readings/raw/informe.pdf`).
  - `collection`: Nombre de la colección destino (ej. `applied_econometrics_2026`, `marco_normativo`, `global_knowledge`).

### Paso 3: Verificación y Búsqueda Semántica
Confirmar que el contenido ha sido indexado correctamente ejecutando búsquedas semánticas directas.
- **Herramienta**: `capital-rag:rag_search`
- **Parámetros**:
  - `query`: Término de búsqueda en lenguaje natural (ej. "determinantes de la informalidad laboral en Ecuador").
  - `collection`: Nombre de la colección donde se realizó la ingesta.
  - `n_results`: Opcional (por defecto 5, máx 20).

### Paso 4: Auditoría de Declaraciones Académicas (Opcional)
Para validar la coherencia y robustez de afirmaciones académicas contra la literatura recientemente ingesta:
- **Herramienta**: `capital-rag:rag_audit_sentence`
- **Parámetros**:
  - `sentence`: Afirmación o declaración académica exacta a auditar.
  - `collection`: Colección de referencias (por defecto `global_knowledge`).

---

## 4. Manejo de Errores y Excepciones

- **Colección Inexistente**: Si se especifica una colección incorrecta en `rag_ingest_file`, verificar las colecciones declaradas activas listadas en `rag_search` (ej. `economic_policy`, `applied_econometrics_2026`, `doble_informalidad`, etc.).
- **Error en Lectura de Archivos**: Asegurarse de proveer rutas **absolutas** al parámetro `file_path` ya que el servidor MCP opera en un entorno sandboxed o con rutas relativas específicas al workspace.

---

## 5. Outputs Esperados

- Confirmación exitosa de la indexación semántica en la colección del vault soberano.
- Disponibilidad del conocimiento para búsquedas semánticas y auditoría de oraciones mediante los endpoints del exocórtex.
