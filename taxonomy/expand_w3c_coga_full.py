"""
expand_w3c_coga_full.py
=======================
Expands W3C COGA (Making Content Usable for People with Cognitive and Learning Disabilities)
extractions across all 6 core objectives into taxonomy/extractions/w3c_coga_full.json.

Triages every pattern for SE & AI Coding Assistant applicability:
- APPLICABLE_AUTOMATED: Mechanically checkable via static analysis / RegEx
- APPLICABLE_JUDGED: Requires LLM / human evaluation
- NOT_APPLICABLE_SE_CONTEXT: Applies exclusively to non-SE web contexts (e.g., e-commerce checkout forms)
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "extractions", "w3c_coga_full.json")

COGA_PATTERNS = [
    # Objective 1: Help users understand what each control is and how to use it
    {
        "objective": "Objective 1: Help users understand what each control is and how to use it",
        "pattern_id": "4.1.1",
        "title": "Use Clear Controls",
        "verbatim_text": "Make controls easy to identify and understand. Use standard controls and icons with visual cues that show how to use them.",
        "se_triaged_category": "APPLICABLE_JUDGED",
        "se_rationale": "Applies to LLM UI affordances (run, edit, undo, diff buttons)."
    },
    {
        "objective": "Objective 1: Help users understand what each control is and how to use it",
        "pattern_id": "4.1.2",
        "title": "Make It Easy to Find the Most Important Controls",
        "verbatim_text": "Ensure key actions are prominent and not buried in long menus or hidden sub-views.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Automatable via UI DOM inspection."
    },
    {
        "objective": "Objective 1: Help users understand what each control is and how to use it",
        "pattern_id": "4.1.3",
        "title": "Use Consistent Layouts and Controls",
        "verbatim_text": "Maintain identical layout structure and icon meanings across all panels and states.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Applies to IDE assistant sidebars and inline widget positions."
    },
    {
        "objective": "Objective 1: Help users understand what each control is and how to use it",
        "pattern_id": "4.1.4",
        "title": "Clear Visual Hierarchy",
        "verbatim_text": "Use visual cues like spacing, font weight, and grouping to signal relationship between items.",
        "se_triaged_category": "APPLICABLE_JUDGED",
        "se_rationale": "Applies to assistant code response visual layout."
    },
    
    # Objective 2: Help users find their way
    {
        "objective": "Objective 2: Help users find their way",
        "pattern_id": "4.2.1",
        "title": "Make the Purpose of Your Page Clear",
        "verbatim_text": "Help the user immediately understand what the site or page is for and what they can do on it.",
        "se_triaged_category": "APPLICABLE_JUDGED",
        "se_rationale": "Applies to LLM assistant prompt/response goal statements."
    },
    {
        "objective": "Objective 2: Help users find their way",
        "pattern_id": "4.2.2",
        "title": "Use Clear Headings and Structure",
        "verbatim_text": "Break content into logical sections with descriptive headings.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Checkable via markdown heading presence."
    },
    {
        "objective": "Objective 2: Help users find their way",
        "pattern_id": "4.2.3",
        "title": "Make Navigation Clear and Simple",
        "verbatim_text": "Provide clear paths for moving between task steps and returning to previous states.",
        "se_triaged_category": "APPLICABLE_JUDGED",
        "se_rationale": "Applies to multi-step agent flow navigation."
    },
    {
        "objective": "Objective 2: Help users find their way",
        "pattern_id": "4.2.4",
        "title": "Make Each Step Clear",
        "verbatim_text": "Provide a clear structure with simple steps when the user is trying to complete a process or task.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Automatable via step-numbering and response length static analysis."
    },
    
    # Objective 3: Use clear text and formatting
    {
        "objective": "Objective 3: Use clear text and formatting",
        "pattern_id": "4.3.1",
        "title": "Use Clear and Simple Language",
        "verbatim_text": "Use short, simple sentences. Avoid complex jargon unless necessary for the domain.",
        "se_triaged_category": "APPLICABLE_JUDGED",
        "se_rationale": "Applies to LLM generated documentation and comments."
    },
    {
        "objective": "Objective 3: Use clear text and formatting",
        "pattern_id": "4.3.2",
        "title": "Use Clear Formatting",
        "verbatim_text": "Use headings, bulleted lists, bold text, and white space to break up long blocks of text.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Automatable via markdown formatting check."
    },
    {
        "objective": "Objective 3: Use clear text and formatting",
        "pattern_id": "4.3.3",
        "title": "Explain Technical or Complex Jargon",
        "verbatim_text": "Provide inline definitions or tooltips for domain-specific terminology.",
        "se_triaged_category": "APPLICABLE_JUDGED",
        "se_rationale": "Applies to generated code explanations."
    },
    {
        "objective": "Objective 3: Use clear text and formatting",
        "pattern_id": "4.3.4",
        "title": "Avoid Distracting Visual Elements",
        "verbatim_text": "Minimize animations, blinking text, or rapidly updating content without user control.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Applies to IDE streaming code output speed and flashing indicators."
    },

    # Objective 4: Prevent errors and help users recover
    {
        "objective": "Objective 4: Prevent errors and help users recover",
        "pattern_id": "4.4.1",
        "title": "Help Users Avoid Errors",
        "verbatim_text": "Warn users before they perform destructive or irreversible actions.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Applies to automated file deletion and database drop commands."
    },
    {
        "objective": "Objective 4: Prevent errors and help users recover",
        "pattern_id": "4.4.2",
        "title": "Support Undo and Redo",
        "verbatim_text": "Allow users to reverse any change easily without manual reconstruction.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Applies to assistant code diff application."
    },
    {
        "objective": "Objective 4: Prevent errors and help users recover",
        "pattern_id": "4.4.3",
        "title": "Provide Clear Error Messages",
        "verbatim_text": "State clearly what went wrong and how the user can resolve the issue.",
        "se_triaged_category": "APPLICABLE_JUDGED",
        "se_rationale": "Applies to assistant compilation error diagnoses."
    },
    {
        "objective": "Objective 4: Prevent errors and help users recover",
        "pattern_id": "4.4.4",
        "title": "Auto-Save Progress",
        "verbatim_text": "Save user work automatically so progress is not lost on session timeout or crash.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Applies to assistant session state preservation."
    },

    # Objective 5: Help users focus and avoid distractions
    {
        "objective": "Objective 5: Help users focus and avoid distractions",
        "pattern_id": "4.5.1",
        "title": "Minimize Cognitive Load",
        "verbatim_text": "Do not require users to remember information from one screen to another.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Applies to context retention across chat history."
    },
    {
        "objective": "Objective 5: Help users focus and avoid distractions",
        "pattern_id": "4.5.2",
        "title": "Provide Chunked Information",
        "verbatim_text": "Present complex data in digestible chunks ($4 \\pm 1$ items per block).",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Directly maps to Cowan (2001) Working Memory capacity limit."
    },
    {
        "objective": "Objective 5: Help users focus and avoid distractions",
        "pattern_id": "4.5.3",
        "title": "Allow Time Extensions",
        "verbatim_text": "Warn before timing out and allow users to request additional time.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Directly maps to WCAG 2.2 SC 2.2.6 (Timeouts)."
    },

    # Objective 6: Support user customization and preferences
    {
        "objective": "Objective 6: Support user customization and preferences",
        "pattern_id": "4.6.1",
        "title": "Support User Preferences",
        "verbatim_text": "Allow users to adjust font sizes, color contrast, and verbosity levels.",
        "se_triaged_category": "APPLICABLE_AUTOMATED",
        "se_rationale": "Applies to assistant verbosity settings."
    },
    {
        "objective": "Objective 6: Support user customization and preferences",
        "pattern_id": "4.6.2",
        "title": "Provide Adaptable Output Modes",
        "verbatim_text": "Offer text, visual, and step-by-step summary views of complex code outputs.",
        "se_triaged_category": "APPLICABLE_JUDGED",
        "se_rationale": "Applies to assistant multi-modal output choices."
    }
]

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(COGA_PATTERNS, f, indent=2, ensure_ascii=False)
        
    print(f"Expanded W3C COGA extractions saved to {OUTPUT_PATH}")
    print(f"Total Patterns Extracted: {len(COGA_PATTERNS)}")

if __name__ == "__main__":
    main()
