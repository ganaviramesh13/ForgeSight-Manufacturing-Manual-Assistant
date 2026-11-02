# Architecture and data flow

```text
User -> Bootstrap UI -> Django auth/role gate -> /ask/
                                      -> Machine-filtered Passage retrieval
PDF -> PyMuPDF -> Manual + Passage(page_number, machine, document, revision)
Answer -> Question(status) -> Citation(passage) -> clickable PDF link
```

`Manual.machine` is the isolation boundary. Retrieval starts with `Passage.objects.filter(manual__machine=machine)` and citations are generated only from those records. The supplied brief, metadata CSV, and START_HERE file are never ingested by the upload workflow.
