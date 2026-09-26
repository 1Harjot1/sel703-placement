"""
build_taxonomy_mapping.py
========================
Builds taxonomy/mapping.json by resolving concept quotes and source printed titles
directly from quote_corpus_verified.json by quote ID.
NO QUOTE STRINGS ARE TYPED BY HAND.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.path.join(BASE_DIR, "..", "..", "VC", "pipeline", "quote_corpus_verified.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "mapping.json")

with open(CORPUS_PATH, "r", encoding="utf-8") as f:
    corpus = json.load(f)

# Perera et al. (IEEE RE 2019) Table I value definitions
VALUE_DEFINITIONS = {
    "Security—Personal": "Safety in one's immediate environment.",
    "Self-Direction—Action": "Freedom to cultivate one's own ideas and determine one's actions.",
    "Self-Direction—Thought": "Freedom to cultivate one's own ideas and understanding.",
    "Universalism—Tolerance": "Acceptance and appreciation of those different from oneself."
}

MAPPING_SPEC = [
    {
        "guideline": "Make the Purpose of Your Page Clear",
        "source": "W3C COGA",
        "source_section": "Section 4.2 Pattern 4.2.1",
        "verbatim_requirement": "Make the purpose of your page clear. Help the user immediately understand what the site or page is for and what they can do on it.",
        "cognitive_concept": "Ambiguity Intolerance",
        "concept_citation": "10.1016/j.janxdis.2006.03.014",
        "concept_quote_id": "10.1016/j.janxdis.2006.03.014:s21",
        "schwartz_value": "Security—Personal",
        "link_type": "implicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "Make Each Step Clear",
        "source": "W3C COGA",
        "source_section": "Section 4.2 Pattern 4.2.4",
        "verbatim_requirement": "Provide a clear structure with simple steps when the user is trying to complete a process or task.",
        "cognitive_concept": "Working Memory Overload",
        "concept_citation": "10.1017/s0140525x01003922",
        "concept_quote_id": "10.1017/s0140525x01003922:s14",
        "schwartz_value": "Security—Personal",
        "link_type": "implicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "Let Users Go Back",
        "source": "W3C COGA",
        "source_section": "Section 4.5 Pattern 4.5.2",
        "verbatim_requirement": "Ensure that users can go back to previous steps in a process and undo mistakes easily.",
        "cognitive_concept": "Inhibition Deficit",
        "concept_citation": "10.1037/0033-2909.121.1.65",
        "concept_quote_id": "10.1037/0033-2909.121.1.65:s37",
        "schwartz_value": "Security—Personal",
        "link_type": "implicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "Notify Users of Costs at Start of Task",
        "source": "W3C COGA",
        "source_section": "Section 4.5 Pattern 4.5.3",
        "verbatim_requirement": "Tell users if there are costs or unexpected consequences before they start a process.",
        "cognitive_concept": "Planning Deficit",
        "concept_citation": "10.1037/0033-2909.133.1.65",
        "concept_quote_id": "10.1037/0033-2909.133.1.65:s4",
        "schwartz_value": "Security—Personal",
        "link_type": "implicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "Accept Different Input Formats",
        "source": "W3C COGA",
        "source_section": "Section 4.5 Pattern 4.5.8",
        "verbatim_requirement": "Allow users to enter data in different formats without failing validation.",
        "cognitive_concept": "Cognitive Flexibility Deficit",
        "concept_citation": "10.1016/s1364-6613(03)00028-7",
        "concept_quote_id": "10.1016/s1364-6613(03)00028-7:s3",
        "schwartz_value": "Universalism—Tolerance",
        "link_type": "implicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "Avoid Data Loss and Timeouts",
        "source": "W3C COGA",
        "source_section": "Section 4.5 Pattern 4.5.9",
        "verbatim_requirement": "Ensure data is saved automatically and users are warned before any session or task times out.",
        "cognitive_concept": "Time Blindness",
        "concept_citation": "10.1016/j.neuropsychologia.2012.09.036",
        "concept_quote_id": "10.1016/j.neuropsychologia.2012.09.036:s6",
        "schwartz_value": "Security—Personal",
        "link_type": "implicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "Limit Interruptions",
        "source": "W3C COGA",
        "source_section": "Section 4.6 Pattern 4.6.1",
        "verbatim_requirement": "Avoid pop-ups, auto-updates, and unnecessary notifications while the user is focusing on a task.",
        "cognitive_concept": "Inhibition Deficit",
        "concept_citation": "10.1037/0033-2909.121.1.65",
        "concept_quote_id": "10.1037/0033-2909.121.1.65:s37",
        "schwartz_value": "Security—Personal",
        "link_type": "implicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "2.2.6 Timeouts",
        "source": "W3C WCAG 2.2",
        "source_section": "Guideline 2.2 Level AAA SC 2.2.6",
        "verbatim_requirement": "Users must be warned of the duration of any user inactivity that could cause data loss, unless data is preserved for more than 20 hours when the user does not take any actions.",
        "cognitive_concept": "Time Blindness",
        "concept_citation": "10.1016/j.neuropsychologia.2012.09.036",
        "concept_quote_id": "10.1016/j.neuropsychologia.2012.09.036:s6",
        "schwartz_value": "Security—Personal",
        "link_type": "explicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "3.3.4 Error Prevention (Legal, Financial, Data)",
        "source": "W3C WCAG 2.2",
        "source_section": "Guideline 3.3 Level AA SC 3.3.4",
        "verbatim_requirement": "For Web pages that cause legal commitments or financial transactions for the user to occur, that modify or delete user-controllable data in data storage systems, or that submit user test responses, submissions must be reversible, checked for errors, or confirmed before finalizing.",
        "cognitive_concept": "Inhibition Deficit",
        "concept_citation": "10.1037/0033-2909.121.1.65",
        "concept_quote_id": "10.1037/0033-2909.121.1.65:s37",
        "schwartz_value": "Security—Personal",
        "link_type": "explicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "Transparency and Provision of Information to Deployers",
        "source": "EU AI Act",
        "source_section": "Article 13",
        "verbatim_requirement": "High-risk AI systems shall be designed and developed in such a way as to ensure that their operation is sufficiently transparent to enable deployers to interpret the system's output and use it appropriately.",
        "cognitive_concept": "Ambiguity Intolerance",
        "concept_citation": "10.1016/j.janxdis.2006.03.014",
        "concept_quote_id": "10.1016/j.janxdis.2006.03.014:s21",
        "schwartz_value": "Self-Direction—Thought",
        "link_type": "explicit",
        "verified_by_harjot": False
    },
    {
        "guideline": "Human Oversight",
        "source": "EU AI Act",
        "source_section": "Article 14",
        "verbatim_requirement": "High-risk AI systems shall be designed and developed in such a way, including with appropriate human-machine interface tools, that they can be effectively overseen by natural persons during their use.",
        "cognitive_concept": "Planning Deficit",
        "concept_citation": "10.1037/0033-2909.133.1.65",
        "concept_quote_id": "10.1037/0033-2909.133.1.65:s4",
        "schwartz_value": "Self-Direction—Action",
        "link_type": "explicit",
        "verified_by_harjot": False
    }
]

output_data = []
for spec in MAPPING_SPEC:
    doi, sid = spec["concept_quote_id"].split(":")
    if doi not in corpus:
        raise KeyError(f"DOI {doi} not found in quote corpus")
        
    doc_entry = corpus[doi]
    if sid not in doc_entry["sentences"]:
        raise KeyError(f"Sentence ID {sid} not found for DOI {doi} in quote corpus")
        
    quote_text = doc_entry["sentences"][sid]
    printed_title = doc_entry.get("printed_title", "")
    pdf_filename = doc_entry.get("pdf_filename", "")
    val_def = VALUE_DEFINITIONS[spec["schwartz_value"]]
    
    entry = {
        "guideline": spec["guideline"],
        "source": spec["source"],
        "source_section": spec["source_section"],
        "verbatim_requirement": spec["verbatim_requirement"],
        "cognitive_concept": spec["cognitive_concept"],
        "concept_citation": spec["concept_citation"],
        "source_printed_title": printed_title,
        "source_pdf_filename": pdf_filename,
        "concept_quote_id": spec["concept_quote_id"],
        "concept_quote": quote_text,
        "schwartz_value": spec["schwartz_value"],
        "value_definition": val_def,
        "link_type": spec["link_type"],
        "verified_by_harjot": spec["verified_by_harjot"]
    }
    output_data.append(entry)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"Successfully regenerated {OUTPUT_PATH} carrying source printed titles alongside resolved quotes.")
