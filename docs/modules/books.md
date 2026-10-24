# Books Module (`tangkhul_lib.books`)

The **Books** module is a planned domain module dedicated to cataloguing and analyzing Tangkhul textbooks, grammatical studies, historical publications, and literary books.

---

## Planned Scope & Objectives

- **Resource Cataloguing**: Maintain comprehensive bibliographic metadata in `data/manifests/books.jsonl`.
- **Digitization & Extraction**: Parse permitted, out-of-copyright or authorized texts (e.g., historical mission publications, educational readers).
- **Sentence & Vocabulary Extraction**: Extract running sentences and vocabulary items, linking each word occurrence to its source book ID, page number, and paragraph.
- **Grammar & Orthography Analysis**: Study historical changes in Tangkhul spelling conventions across different publication eras.

---

## Current Status (Step 1)

- Architecture and directory structures initialized.
- Manifest schema supported in `books.jsonl`.
- Text parsing and full extraction pipelines will be implemented in subsequent steps.
