# Diagrama de Sendero (Path Diagram) - SEM Homicidios

Este diagrama representa la interdependencia de las variables en el Sistema de Ecuaciones Simultáneas de Homicidios para Ecuador.

```mermaid
graph LR
    %% Nodos
    R[Remesas % PIB]
    U[Uso Internet %]
    D[Desempleo Total]
    G[Gasto Militar % PIB]
    H[Homicidios 100k]

    %% Ecuación 2: Desempleo (Variable Endógena)
    R --> D
    U --> D

    %% Ecuación 1: Homicidios (Variable Endógena)
    D --> H
    G --> H
    R --> H

    %% Estilos
    style H fill:#f96,stroke:#333,stroke-width:4px
    style D fill:#6bf,stroke:#333,stroke-width:2px
    style R fill:#dfd,stroke:#333
    style U fill:#dfd,stroke:#333
    style G fill:#dfd,stroke:#333
```

## Instrucciones para Visio
1. Copie el código Mermaid anterior.
2. Utilice el sitio [Mermaid Live Editor](https://mermaid.live/) para previsualizar.
3. Exporte como **SVG**.
4. Importe el archivo SVG en Microsoft Visio para darle el formato final institucional.
