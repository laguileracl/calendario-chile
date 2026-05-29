# PUBLICATION_CHECKLIST — calendario-chile

Lista de verificación previa a cualquier publicación pública. **Mientras existan ítems sin marcar, NO publicar.**

## 1. Licencia y derechos — ✅ RESUELTO: MIT

- [x] Licencia única **MIT** para toda la superficie pública (código, datos, documentación, schemas, API, derivados). Titular: Luis Aguilera, 2026.
- [x] `LICENSE` (MIT) creado; `LICENSE_DRAFT.md` movido a `data/internal/audit/OBSOLETE_LICENSE_DRAFT.md`.
- [x] `pyproject.toml` (`license = MIT`), `schema/datapackage.json` (`licenses: MIT`) y `data/api/v1/metadata.json` (`license: MIT`) actualizados.
- Ver `reports/LICENSE_DECISION_REPORT.md`.

## 2. Atribución y terceros

- [x] `make clean-check` sin coincidencias en zonas públicas.
- [x] Documentación pública redactada como *fuentes internas del proyecto procesadas*.
- [ ] Revisar `data/internal/audit/REVIEW_THIRD_PARTY_REFERENCES.md` (referencias internas).
- [ ] Confirmar que ningún archivo a publicar proviene de `data/internal/raw/` sin revisión.

## 3. Calidad de datos

- [x] 10/10 tests de validación.
- [x] Cobertura 1981–2100 completa; 0 duplicados exactos.
- [ ] Revisar 665 eventos `low-confidence`.
- [ ] Revisar 31 feriados/bancarios sin fundamento legal mapeado.
- [ ] Revisar `category = other` en conmemorativos (clasificación temática pendiente).

## 4. Peso del repositorio y distribución

- [ ] Decidir qué se versiona vs. qué se distribuye por **GitHub Releases / Pages / LFS**.
- [ ] Confirmar exclusiones de `.gitignore` (bulk regenerable excluido por defecto).
- [ ] ¿Publicar **SQLite/Parquet** o sólo derivados livianos (JSON/CSV/ICS)?
- [ ] ¿Publicar **fuentes brutas** (`data/internal/raw/`) o mantenerlas privadas?

## 5. Contrato e interoperabilidad

- [x] JSON Schema y Frictinless datapackage generados.
- [ ] Validar muestras contra el esquema en CI antes de release.
- [ ] Fijar política de versionado del esquema (semver).

## 6. Términos y avisos

- [x] Aviso "no constituye asesoría legal" en README y `docs/legal_notes.md`.
- [ ] Revisar términos legales finales con la decisión de licencia.

## 7. Operación

- [x] Workflows de CI (`validate.yml`, `build.yml`).
- [ ] Configurar publicación de API estática (Pages) si se aprueba.
- [ ] Definir cadencia de regeneración y proceso de PRs automáticos.
