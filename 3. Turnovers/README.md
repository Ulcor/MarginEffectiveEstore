

```mermaid


flowchart TD
A[Supplyer] --> B{Distribution Center}
B -- Magistral Courier Team --> C[Warehouse Local. Area 1]
B -- Magistral Courier Team --> D[Warehouse Local. Area 2]
C --> F[Courier Team. Area 1]
D --> H[Courier Team. Area 2]
H -- Turnover --> A
```