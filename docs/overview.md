# Overview

## Visión

Ser el **dataset abierto de referencia del calendario chileno**: completo, correcto, trazable y fácil de consumir por máquinas, cubriendo tanto los feriados con efectos legales como la capa conmemorativa (días, semanas, meses y años nacionales).

## Por qué

Las soluciones existentes para calendarios de feriados suelen cubrir pocos años, no distinguen dimensiones propias de Chile (irrenunciabilidad y su categoría, feriados bancarios), no incorporan la capa conmemorativa ni el fundamento legal, y rara vez ofrecen el dato en múltiples formatos abiertos listos para integrar.

## Alcance

- **Temporal:** 1981–2100.
- **Temático:** feriados públicos, bancarios, locales, de ámbito restringido y eventos conmemorativos.
- **Dimensiones:** fecha(s), tipo, categoría, alcance territorial (ISO 3166-2), irrenunciabilidad, recurrencia, movilidad de fecha y fundamento legal.

## Diferenciadores

- **Irrenunciabilidad** con categoría 1–5 (régimen laboral chileno).
- **Feriados bancarios** como dimensión propia.
- **Capa conmemorativa** extensa.
- **Cobertura de 120 años** (histórica y proyectada).
- **Fundamento legal** trazable a la norma y, cuando existe, a su ficha oficial.

## Casos de uso

- Cálculo de **días hábiles** y vencimientos (legal, financiero, RR.HH.).
- Integraciones en software (banca, e-commerce, logística, agendas).
- Investigación y periodismo de datos sobre la evolución del calendario.
- Suscripción a calendarios `.ics`.

## Principios de diseño

1. **Trazabilidad:** cada dato es reproducible desde las fuentes internas.
2. **No inventar:** lo ausente queda `null`; las inferencias se marcan.
3. **Interoperar:** vocabulario alineado a estándares (ISO 3166-2, RFC 5545, JSON Schema, Frictionless).
4. **Separar** datos públicos, material interno y pipeline.
