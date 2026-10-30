# Research & Cultural Articles Module (`tangkhul_lib.articles`)

The **Articles** module provides comprehensive bibliographic cataloguing, metadata validation, text extraction, linguistic analysis, and high-level retrieval for scholarly, linguistic, and cultural articles published in and about the Tangkhul language.

---

## 1. Module Purpose

Tangkhul linguistic and cultural research spans more than a century of scholarship, ranging from early comparative Tibeto-Burman studies to modern laboratory phonetics, computational natural language processing (NLP), ethnolinguistic ritual documentation, and customary jurisprudence.

The primary purposes of `tangkhul_lib.articles` are:
1. **Academic Preservation**: Systematically catalogue peer-reviewed articles, doctoral research monographs, conference proceedings, and cultural bulletins in [`data/manifests/articles.jsonl`](file:///f:/tangkhul-language-library/data/manifests/articles.jsonl).
2. **Linguistic Data Integration**: Digitize full article texts with section headings, interlinear glossed examples, phonetic measurements, and bibliographies.
3. **Multi-Format Distribution**: Provide complete individual article downloads in both structured JSON ([`data/exports/articles/{id}.json`](file:///f:/tangkhul-language-library/data/exports/articles)) and multi-page printable PDF format ([`data/exports/articles/{id}.pdf`](file:///f:/tangkhul-language-library/data/exports/articles)), as well as master consolidated compendiums ([`data/exports/articles.json`](file:///f:/tangkhul-language-library/data/exports/articles.json) and [`data/exports/articles.pdf`](file:///f:/tangkhul-language-library/data/exports/articles.pdf)).
4. **Search and Query API**: Enable programmatic search by author, linguistic subfield, keywords, and text occurrences.

---

## 2. Catalogued Research Articles (10 Volumes)

| ID | Title | Authors | Journal / Venue | Year | Subject |
|---|---|---|---|---|---|
| `ART-LING-001` | [Comparative Tangkhul: Lexical and Phonological Reconstruction](file:///f:/tangkhul-language-library/data/exports/articles/ART-LING-001.pdf) | David R. Mortensen, Jennifer Keogh | UC Berkeley STEDT Monograph Series | 2003 | Comparative Linguistics & Dialectology |
| `ART-LING-002` | [A Reconstruction of Proto-Tangkhulic Rhymes](file:///f:/tangkhul-language-library/data/exports/articles/ART-LING-002.pdf) | David R. Mortensen, James A. Miller | Linguistics of the Tibeto-Burman Area (LTBA 36.1) | 2013 | Historical Phonology & Coda Rhymes |
| `ART-LING-003` | [Tangkhul Naga and Comparative Tibeto-Burman](file:///f:/tangkhul-language-library/data/exports/articles/ART-LING-003.pdf) | Prof. James A. Matisoff | STEDT Monograph Paper No. 1, UC Berkeley | 1972 | Sino-Tibetan Etymology & Prefixes |
| `ART-LING-004` | [Tangkhul-Naga Grammar: Word Formation & Morphology](file:///f:/tangkhul-language-library/data/exports/articles/ART-LING-004.pdf) | Dr. Victor Ahum | Manipur University Ph.D. Dissertation | 1997 | Descriptive Morphology & Syntax |
| `ART-LING-005` | [Aspiration Dissimilation & Phonological Rules in Tangkhul](file:///f:/tangkhul-language-library/data/exports/articles/ART-LING-005.pdf) | Deepthi Gopal | Carnegie Mellon University Working Papers | 2016 | Experimental Acoustic Phonetics |
| `ART-LING-006` | [Towards Morphological Processing & NLP for Tangkhul](file:///f:/tangkhul-language-library/data/exports/articles/ART-LING-006.pdf) | Richard Luikham, Dr. Ninghorla Zimik, Dr. Kh. Raju Singh | Computational Linguistics & NLP (arXiv:2009.07124) | 2020 | Computational Morphology & Corpus NLP |
| `ART-LING-007` | [Echo Word Formation and Reduplicative Morphology](file:///f:/tangkhul-language-library/data/exports/articles/ART-LING-007.pdf) | Dr. S. Arokianathan | Indian Linguistics (LSI Pune, Vol. 45) | 1984 | Expressive Morphology & Ideophones |
| `ART-LING-008` | [Tone System and Pitch Accent in Standard Ukhrul Tangkhul](file:///f:/tangkhul-language-library/data/exports/articles/ART-LING-008.pdf) | Dr. Kapesa Khayi, Prof. K. V. Subbarao | Language in India & NEILS Bulletin (Vol. 12) | 2012 | Tonology & Fundamental Frequency (F0) |
| `ART-CULT-001` | [Tangkhul Luira Phanit & Ancient Agricultural Invocations](file:///f:/tangkhul-language-library/data/exports/articles/ART-CULT-001.pdf) | Prof. Khashim Ruivah | Journal of NEICSSR & TRI Manipur | 1987 | Ethnolinguistics & Agricultural Rituals |
| `ART-CULT-002` | [Tangkhul Hao Ngashan: Customary Law & Social Governance](file:///f:/tangkhul-language-library/data/exports/articles/ART-CULT-002.pdf) | T. Luikham, A. S. W. Shimray, Wung Cultural Forum | Tribal Jurisprudence Bulletin of Manipur | 2004 | Customary Law & Clan Exogamy |

---

## 3. Python API Usage

```python
from tangkhul_lib.articles.catalogue import ArticleCatalogue, get_all_articles, get_article

# 1. Retrieve full article catalogue
catalogue = ArticleCatalogue.load_default()

# 2. Search by author
mortensen_articles = catalogue.search(author="Mortensen")
for a in mortensen_articles:
    print(a.id, a.title, a.publication_year)

# 3. Search by linguistic query or keywords
tone_articles = catalogue.search(query="tone")

# 4. Retrieve complete article with all sections, data, and references
article = get_article("ART-LING-001")
print(article["title"])
print("Sections count:", len(article["sections"]))
print("Abstract:", article["abstract"])
```

---

## 4. Download and Export File Structure

All digitalized research articles are available in the repository at:
* **Dedicated Manifest**: [`data/manifests/articles.jsonl`](file:///f:/tangkhul-language-library/data/manifests/articles.jsonl)
* **Master JSON Compendium**: [`data/exports/articles.json`](file:///f:/tangkhul-language-library/data/exports/articles.json)
* **Master Multi-Page PDF**: [`data/exports/articles.pdf`](file:///f:/tangkhul-language-library/data/exports/articles.pdf)
* **Individual JSON Exports**: `data/exports/articles/{id}.json`
* **Individual PDF Exports**: `data/exports/articles/{id}.pdf`
* **Plain Text Corpus**: `data/raw/articles/{id}.txt`
