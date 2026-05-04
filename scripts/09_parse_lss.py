"""Parse LimeSurvey .lss files into structured Slovak text suitable for Appendix A.

Output format per question:
  Q-code | Type | Group | Mandatory | Question text
  Optional sub-questions (for multi-question batteries)
  Optional answer options
"""
import xml.etree.ElementTree as ET
import sys
from pathlib import Path
from collections import defaultdict

TYPE_LABELS_SK = {
    "T": "Voľný textový vstup (dlhý)",
    "S": "Voľný textový vstup (krátky)",
    "U": "Voľný textový vstup (veľmi dlhý)",
    "N": "Numerický vstup",
    "K": "Viac numerických vstupov",
    "L": "Výber z možností (jedna odpoveď)",
    "!": "Výber z rozbaľovacieho zoznamu",
    "M": "Viacnásobný výber (zaškrtávacie políčka)",
    "P": "Viacnásobný výber s komentárom",
    "F": "Pole (Likertova matica)",
    "A": "Pole 5-bodová Likertova škála",
    "B": "Pole 10-bodová Likertova škála",
    "1": "Pole s dvoma škálami",
    "Y": "Áno / Nie",
    "G": "Pohlavie",
    "X": "Textový blok (bez odpovede)",
    "*": "Equation",
    ":": "Pole numerických vstupov",
    ";": "Pole textov",
}


def cdata(node):
    if node is None:
        return ""
    return (node.text or "").strip()


def parse_lss(path):
    tree = ET.parse(path)
    root = tree.getroot()

    # Build language map
    lang = "sk"

    # Groups
    groups = {}
    for row in root.findall(".//groups/rows/row"):
        gid = cdata(row.find("gid"))
        order = cdata(row.find("group_order"))
        groups[gid] = {"gid": gid, "order": int(order) if order else 0}

    # Group L10n (names)
    for row in root.findall(".//group_l10ns/rows/row"):
        gid = cdata(row.find("gid"))
        name = cdata(row.find("group_name"))
        desc = cdata(row.find("description"))
        if gid in groups:
            groups[gid]["name"] = name
            groups[gid]["description"] = desc

    # Questions
    questions = {}
    for row in root.findall(".//questions/rows/row"):
        qid = cdata(row.find("qid"))
        parent = cdata(row.find("parent_qid"))
        gid = cdata(row.find("gid"))
        qtype = cdata(row.find("type"))
        title = cdata(row.find("title"))
        order = cdata(row.find("question_order"))
        mandatory = cdata(row.find("mandatory"))
        scale = cdata(row.find("scale_id")) or "0"
        questions[qid] = {
            "qid": qid,
            "parent": parent or "0",
            "gid": gid,
            "type": qtype,
            "title": title,
            "order": int(order) if order else 0,
            "mandatory": mandatory == "Y",
            "scale": int(scale) if scale else 0,
            "text": "",
            "subquestions": [],
            "answers": [],
        }

    # Question L10n (text)
    for row in root.findall(".//question_l10ns/rows/row"):
        qid = cdata(row.find("qid"))
        text = cdata(row.find("question"))
        if qid in questions:
            questions[qid]["text"] = text

    # Sub-questions are stored in a separate <subquestions> section in newer LSS
    sub_qs = defaultdict(list)
    for row in root.findall(".//subquestions/rows/row"):
        sqid = cdata(row.find("qid"))
        parent = cdata(row.find("parent_qid"))
        title = cdata(row.find("title"))
        order = cdata(row.find("question_order"))
        scale = cdata(row.find("scale_id")) or "0"
        sub = {
            "qid": sqid,
            "parent": parent,
            "title": title,
            "order": int(order) if order else 0,
            "scale": int(scale) if scale else 0,
            "text": "",
        }
        sub_qs[parent].append(sub)
        # Also keep them lookup-able by qid for L10n attachment below
        questions.setdefault(sqid, sub.copy())

    # Question L10n now also covers sub-question text (already loaded above);
    # since sub-questions are not in `questions` originally, fetch from L10n by qid:
    for row in root.findall(".//question_l10ns/rows/row"):
        qid = cdata(row.find("qid"))
        text = cdata(row.find("question"))
        # Update sub-question text in sub_qs
        for parent_id, subs in sub_qs.items():
            for s in subs:
                if s["qid"] == qid:
                    s["text"] = text

    for parent_qid, subs in sub_qs.items():
        subs.sort(key=lambda s: s["order"])
        if parent_qid in questions:
            questions[parent_qid]["subquestions"] = subs

    # Answers
    answers = defaultdict(list)
    for row in root.findall(".//answers/rows/row"):
        qid = cdata(row.find("qid"))
        code = cdata(row.find("code"))
        order = cdata(row.find("sortorder"))
        scale = cdata(row.find("scale_id")) or "0"
        answers[qid].append({"code": code, "order": int(order) if order else 0, "scale": int(scale)})

    # Answer L10n
    for row in root.findall(".//answer_l10ns/rows/row"):
        # The CDATA-wrapped fields: aid, language, answer
        aid_node = row.find("aid")
        ans_text = cdata(row.find("answer"))
        # Need to map aid -> answer in answers dict; LimeSurvey stores aid in answers/rows but not exposed by qid lookup.
        # Re-build via answers/rows: read again with aid mapping
        pass

    # Build aid → text map separately
    aid_text = {}
    for row in root.findall(".//answer_l10ns/rows/row"):
        aid = cdata(row.find("aid"))
        text = cdata(row.find("answer"))
        if aid:
            aid_text[aid] = text

    # Re-parse answers with aid
    answers = defaultdict(list)
    for row in root.findall(".//answers/rows/row"):
        qid = cdata(row.find("qid"))
        aid = cdata(row.find("aid"))
        code = cdata(row.find("code"))
        order = cdata(row.find("sortorder"))
        scale = cdata(row.find("scale_id")) or "0"
        answers[qid].append({
            "aid": aid,
            "code": code,
            "text": aid_text.get(aid, ""),
            "order": int(order) if order else 0,
            "scale": int(scale),
        })

    for qid, lst in answers.items():
        lst.sort(key=lambda a: (a["scale"], a["order"]))
        if qid in questions:
            questions[qid]["answers"] = lst

    return groups, questions


import re as _re


def clean_html(text):
    """Strip embedded <script>...</script>, JS arrays, and basic HTML tags."""
    if not text:
        return ""
    # Strip script tags + content
    text = _re.sub(r"<script[^>]*>.*?</script>", "", text, flags=_re.DOTALL | _re.IGNORECASE)
    # Strip JS-style availableChoices arrays embedded in plain text after script
    text = _re.sub(r"var availableChoices\s*=\s*\[.*?\];", "", text, flags=_re.DOTALL)
    text = _re.sub(r"\$\([^)]*\)\.[^;]+;", "", text, flags=_re.DOTALL)
    # Replace <br /> variants with newline
    text = _re.sub(r"<br\s*/?>", "\n", text, flags=_re.IGNORECASE)
    text = _re.sub(r"<p[^>]*>", "\n", text, flags=_re.IGNORECASE)
    text = _re.sub(r"</p>", "", text, flags=_re.IGNORECASE)
    # Remove all other tags
    text = _re.sub(r"<[^>]+>", "", text)
    # Collapse blank lines
    text = _re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def render_appendix(groups, questions, survey_label):
    lines = []
    lines.append(f"Príloha: Štruktúra dotazníka — {survey_label}")
    lines.append("")

    # Get only top-level questions
    top_qs = [q for q in questions.values() if q["parent"] == "0"]
    by_group = defaultdict(list)
    for q in top_qs:
        by_group[q["gid"]].append(q)

    sorted_groups = sorted(groups.values(), key=lambda g: g.get("order", 0))
    for g in sorted_groups:
        gid = g["gid"]
        if gid not in by_group:
            continue
        lines.append("")
        lines.append(f"## Skupina: {g.get('name','(bez názvu)')}")
        if g.get("description"):
            lines.append(f"_{g['description']}_")
        lines.append("")
        qs = sorted(by_group[gid], key=lambda q: q["order"])
        for q in qs:
            tlabel = TYPE_LABELS_SK.get(q["type"], f"Typ '{q['type']}'")
            mand = " (povinná)" if q["mandatory"] else ""
            text = clean_html(q["text"])
            # Special handling for two free-text items that embed long JS pick-lists
            if q["title"] == "G01Q07":
                text = ("Tvoja stredná škola je: (textový vstup s našepkávačom; "
                        "kompletný zoznam slovenských stredných škôl bol poskytnutý ako "
                        "klientsky autocomplete — nereprodukovaný v tlačovej prílohe.)")
            elif q["title"] == "G01Q20":
                text = ("V ktorom meste žiješ? (textový vstup s našepkávačom obsahujúcim "
                        "zoznam slovenských miest a obcí — nereprodukovaný v tlačovej prílohe.)")
            lines.append(f"### {q['title']}{mand}")
            lines.append(f"_Typ otázky_: {tlabel}")
            lines.append("")
            if text:
                lines.append(text)
                lines.append("")
            # Sub-questions
            if q["subquestions"]:
                lines.append("**Položky (sub-questions):**")
                for s in q["subquestions"]:
                    stext = clean_html(s["text"])
                    lines.append(f"  - `{s['title']}`: {stext}")
                lines.append("")
            # Answers
            if q["answers"]:
                # Group by scale
                scales = defaultdict(list)
                for a in q["answers"]:
                    scales[a["scale"]].append(a)
                for scale_id, ans in scales.items():
                    if len(scales) > 1:
                        lines.append(f"**Škála {scale_id}:**")
                    else:
                        lines.append("**Možnosti odpovede:**")
                    for a in ans:
                        lines.append(f"  - `{a['code']}` — {a['text']}")
                    lines.append("")
            lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    # Paths are resolved relative to the repository root (parent of scripts/).
    # Place the LimeSurvey LSS exports in data/ before running.
    ROOT = Path(__file__).resolve().parents[1]
    base = ROOT / "data"
    out_dir = ROOT / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    files = [
        (base / "limesurvey_survey_777777.lss",
         "Dataset A — Digitálne návyky a používanie mobilných aplikácií",
         out_dir / "Appendix_A_Dataset_A_questionnaire.md"),
        (base / "limesurvey_survey_971496.lss",
         "Dataset B — Digitálne prostredie a smart-city gramotnosť",
         out_dir / "Appendix_A_Dataset_B_questionnaire.md"),
    ]
    for p, label, out_path in files:
        if not p.exists():
            print(f"Skipping {p.name}: not present in data/")
            continue
        groups, questions = parse_lss(p)
        text = render_appendix(groups, questions, label)
        out_path.write_text(text, encoding="utf-8")
        print(f"Written: {out_path} ({len(text)} chars, {len(questions)} questions, {len(groups)} groups)")
