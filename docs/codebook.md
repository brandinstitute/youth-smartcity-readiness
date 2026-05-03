# Codebook

Variable-by-variable reference for the two source surveys and the indicator file. Slovak labels are quoted from the original LimeSurvey export; English labels are the analyst's working translation.

## Dataset A — `results-survey777777 (2).csv`

Mobile-app habits of secondary-school students. Delimiter: `;`. Encoding: UTF-8 with BOM. Total rows in the LimeSurvey export: **135** (134 with a non-null `submitdate`). Of those, **83** identify as secondary-school students; the monograph uses **N = 82** after listwise exclusion of one case missing the gender item, in line with §4.1.

| Column (Slovak label) | English label | Type | Coding |
|---|---|---|---|
| `id. ID odpovede` | Response ID | int | LimeSurvey internal |
| `submitdate. Dátum odoslania` | Submit date | datetime | ISO format |
| `POHLAVIE. Pohlavie:` | Gender | categorical | M / Ž |
| `VEK. Vek:` | Age | int | 14–19 in retained sample |
| `TYPSKOLY. Typ školy:` | School type | string | Free text — gymnasium / vocational / technical |
| `OS. Operačný systém mobilu:` | Operating system | categorical | iOS / Android / iné |
| `ZNACKA. Značka telefónu:` | Phone brand | string | Free text |
| `POCETAPLIK. Koľko máte aktuálne nainštalovaných aplikácií (odhad):` | Apps installed | int | Self-report estimate |
| `G02Q52. Kedy ste si naposledy nainštalovali novú aplikáciu?` | Recency of last install | categorical | Last week / month / longer |
| `POCETAPLIKpouzivam. Koľko používate aspoň raz z nainštalovaných aplikácií (odhad):` | Apps used | int | Self-report estimate |
| `G02Q51. Priemerný čas používania aplikácií denne (okrem hovorov a SMS):` | Daily app time (hours) | float | Self-report estimate |
| `APP1NAZOV` … `APP10NAZOV` | Top-10 named apps | string | Free text |
| `APP1D` … `APP10D` | Days/week each app is used | int | 0–7 |
| Motive items (multiple) | Motives for app use | binary | 1 = checked |

### Derived variables

- **`apps_use_ratio`** = `apps_used` / `apps_installed`. Reported in the monograph as the use-ratio (mean ≈ 0.22).
- **`AEI`** (App Engagement Index) = 0.5 · min-max(time) + 0.3 · min-max(apps_installed) + 0.2 · min-max(recency). Each component is min-max rescaled to 0–100 individually and then weighted; `apps_installed` is used as the portfolio-size proxy (matching Tables 7–8 of the monograph). `apps_used` is descriptively important for the use-ratio but is **not** an AEI input.
- **AEI band**: low (< 33.3), medium (33.3–66.7), high (> 66.7).

## Dataset B — `results-survey971496.csv`

Smart-city perception of secondary-school students. Delimiter: `;`. Encoding: UTF-8 with BOM. Total rows: 401. Subset retained for analysis (valid grade and complete index items): N = 368.

| Column | English label | Type | Coding |
|---|---|---|---|
| `G01Q07` | School (free text — parsing artefacts cleaned in `01_build_indices.py`) | string | — |
| `G01Q08` | Currently a secondary-school student? | categorical | Áno / Nie / NaN |
| `G02Q02` | Grade | int | 1–4 used; rare 5+ excluded as non-mainstream |
| `G01Q03` | Gender | categorical | Muž / Žena |
| `G01Q10` | Role of technology in a smart city | multiple choice | One conceptually correct option ("data + connectivity") |
| `G01Q22` | Was *smart city* covered at school? | categorical | Detail / Briefly / No / Unsure / Don't remember |
| `G01Q23` | Importance of smart-city education | Likert 1–5 | Nepodstatné…Veľmi dôležité |
| `G01Q26[SQ001]` | Internet quality **at school** | Likert 1–5 | drives SDR |
| `G01Q26[SQ002]` | Internet quality **at home** | Likert 1–5 | drives DAE |
| `G01Q26[SQ003]` | Internet quality **in the city** | Likert 1–5 | descriptive only |
| `G01Q26[SQ004]` | Modern equipment **at school** | Likert 1–5 | drives SDR |
| `G05Q18` | Encountered smart-city tech locally? | binary | Áno / Nie |
| `G01Q19[SQ001..021]` | Which smart-city features does your city already have? | multi-check | counts feed `smart_features_count` |
| `G08Q25[SQ001..004]` | Internet-connected devices at home | int (counts) | mobile, media, computer, other; winsorised at 30 |

### Derived indices (full formulas in `01_build_indices.py`)

- **DAE** (Digital Access Environment) — average of z(home_internet) and z(devices_total), then min-max rescaled to 0–100.
- **SDR** (School Digital Readiness) — average of z(school_internet) and z(school_equipment), then min-max rescaled to 0–100.
- **CSA** (Curricular and Smart-City Awareness) — average of four standardised items: school exposure (G01Q22, 3-level), conceptual understanding (G01Q10, binary), perceived importance (G01Q23, Likert), local recognition (G05Q18, binary); rescaled to 0–100.
- **YSCR** (Youth Smart-City Readiness) — 0.5 · CSA + 0.3 · SDR + 0.2 · DAE on the 0–100 scale. The default ("YSCR") replaces missing SDR and DAE with their column means before applying weights, keeping valid N = 368. The listwise sensitivity variant ("YSCR_listwise") drops cases missing any input (~321 valid). Pearson correlation between the two ≈ 0.99; substantive ranking is unchanged.

## Slovak indicator file — `people-smart-cities-indikatory-slovensko.xlsx`

253 Slovak municipalities × 8 regions, covering ≈ 3.3 M residents (≈ 62 % of the population). Multi-sheet workbook with z-scored indicators across the *Smart People* axis: qualifications, lifelong learning, plurality, flexibility, creativity, cosmopolitanism, participation. Used in the monograph for context (Section 6.4-1, 9.1, 10.4) rather than as model input — see `01_build_indices.py` for the clean read.

| Indicator family | Sheet | Local variation |
|---|---|---|
| Qualifications | `kvalifikacia` | Yes — large urban-rural gradient |
| Lifelong learning | `celozivotne_vzdel` | Yes |
| Book loans (per cap.) | `kniznice` | Yes |
| Foreigners (share of pop.) | `cudzinci` | Yes — concentrated in Bratislava and West |
| EU election turnout | `volby_eu` | Yes |
| City election turnout | `volby_obecne` | Yes |
| ISCED 5–6 share | `isced_5_6` | Yes |
| Other | various | Many constant at national value |

## Missing-data handling

- **Listwise deletion** is used inside each first-order index: a respondent missing any input item for AEI / DAE / SDR / CSA is excluded from that index but retained for others.
- Headline valid N values used throughout the monograph: Dataset A — total = 82, AEI valid = 77, apps_used = 80, time = 81. Dataset B — total = 401, mainstream grades 1–4 = 368, DAE valid = 342, SDR valid = 354 (or 341 if both items required), CSA valid = 368, Model 7.2 (CSA ~ DAE + SDR + female + grade) = 332.
- The composite **YSCR** uses light **mean-imputation** for missing SDR and DAE before applying the 0.5 / 0.3 / 0.2 weights, preserving valid N = 368. A listwise variant (`YSCR_listwise`) is computed in parallel as a sensitivity check; it correlates with the default at r ≈ 0.99 and yields substantively identical group rankings.
- Self-reported device counts above 30 are treated as data-entry errors (winsorised to NaN); fewer than five cases are affected.
