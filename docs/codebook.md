# Codebook

Variable-by-variable reference for the two source surveys and the indicator file. Slovak labels are quoted from the original LimeSurvey export; English labels are the analyst's working translation.

## Dataset A — `results-survey777777__2_.csv`

Mobile-app habits of secondary-school students. Delimiter: `;`. Encoding: UTF-8 with BOM. Total rows: 133. Secondary-school subset used in the monograph: N = 82.

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
- **`AEI`** (App Engagement Index) = 0.5 · min-max(time) + 0.3 · min-max(apps_used) + 0.2 · min-max(recency). Range 0–1, then rescaled to 0–100 for tables.
- **AEI band**: low (< 33), medium (33–66), high (> 66).

## Dataset B — `results-survey971496.csv`

Smart-city perception of secondary-school students. Delimiter: `;`. Encoding: UTF-8 with BOM. Total rows: 401. Subset retained for analysis (valid grade and complete index items): N = 368.

| Column | English label | Type | Coding |
|---|---|---|---|
| `G01Q07. Tvoja stredná škola je:` | School | string | Free text — has parsing artefacts; cleaned in `01_build_indices.py` |
| `G01Q08` | Grade | int | 1–4 |
| `G01Q09` | Gender | categorical | M / F |
| `G01Q10` | What is the role of technology in a smart city? | multiple choice | One correct option (data + connectivity) |
| `G01Q11` | Internet quality at home | Likert 1–5 | 1 = very poor → 5 = excellent |
| `G01Q12` | Internet quality at school | Likert 1–5 | 1 = very poor → 5 = excellent |
| `G01Q22` | Was the term *smart city* covered at school? | categorical | Detail / Briefly / No / Don't remember |
| `G01Q23` | Importance of smart-city education | Likert 1–5 | |
| `G05Q18` | Which smart-city features does your city already have? | multiple choice | Public Wi-Fi, integrated transport, smart lighting, etc. |
| `G05Q19` | School equipment quality | Likert 1–5 | |
| `G05Q20` | Devices used at school | multiple choice | |

### Derived indices (full formulas in `01_build_indices.py`)

- **DAE** (Digital Access Environment) — z(home_internet) + z(devices_owned), then rescaled to 0–100.
- **SDR** (School Digital Readiness) — z(school_internet) + z(school_equipment), then rescaled to 0–100.
- **CSA** (Civic Smart-city Awareness) — average of standardised: school exposure (G01Q22), conceptual understanding (G01Q10), perceived importance (G01Q23), local recognition (G05Q18), then rescaled to 0–100.
- **YSCR** (Youth Smart-City Readiness) — 0.5 · CSA + 0.3 · SDR + 0.2 · DAE, on the 0–100 scale.

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

- **Listwise deletion** is used for index construction: a respondent who is missing any input item for an index is excluded from that index but retained for others.
- This produces the headline N values used throughout the monograph: 82 / 77 / 80 / 368 / 354 / 332 / 342.
- No imputation is performed.
