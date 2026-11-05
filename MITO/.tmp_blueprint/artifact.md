# Template Distillation Contract - MITO SFA Mobile Blueprint

## Reference

- Retained reference: `E:\Panda\MITO\.tmp_blueprint\reference.docx`
- Original reference: `C:\Users\SAYID\OneDrive\02. Project\Mito\03. Design\SFA v2\MITO Sales Force Automation - Blue Print V1.0 - Draft.docx`
- SHA-256: `ADD73A5C22BF55F178F9A02CCE648CE259043B6CD132112B984CE3EA96060DA8`
- Size: 20,002,131 bytes.
- Rendered page count: 144 pages.
- Section count: 2.
- Visual evidence: `E:\Panda\MITO\.tmp_blueprint\reference_render\page-001.png` through `page-144.png` and `reference.pdf`.
- Structural evidence: `template-style-evidence.json`, section/style/heading/image/field audit outputs, and `inspect_template.py` output.

## Page System

- A4 portrait: 8.27 x 11.69 inches.
- Section 1 margins: left 1.50 in, right 0.89 in, top 1.00 in, bottom 1.38 in.
- Section 2 margins: left 1.50 in, right 0.89 in, top 1.00 in, bottom 1.00 in.
- Header distance: 0.60 in. Footer distance: 0.51 in.
- Section 1 uses a different first-page header/footer for the cover.
- Section 2 starts on a new page and uses the recurring body header/footer.
- No multi-column or landscape page patterns are used.

## Typography

- Primary family: Arial for body and source styles; the reference contains direct Calibri formatting in some legacy content, which is not required for new SFA content.
- Body: Arial 10 pt, black, justified or left aligned as appropriate, 1.0-1.15 line spacing.
- `BP Head 1`: source-derived black section band with white bold text, approximately 26 pt, page break before.
- `BP Head 2`: Arial bold approximately 18 pt, black, compact spacing.
- `BP Head 3`: Arial bold approximately 16 pt, black, compact spacing.
- Process-table text: Arial 8.5-9 pt; header row bold.
- Cover title: source pattern uses bold approximately 26 pt with centered alignment.
- Cover metadata labels: blue italic bold approximately 9 pt.

## Lists and Tables

- Reuse real Word list numbering from the source when numbered or bulleted lists are required.
- Body process table has five user-approved columns: Activity ID, Activity Name, PIC, Description, Type. The source Notes column is intentionally removed.
- Process-table usable width: 5.88 in. Target widths: 0.78, 1.25, 0.90, 2.10, 0.85 in.
- Header row: medium gray fill, white or black bold text according to source contrast; repeat on page breaks.
- Body rows: white fill, thin black borders, vertically centered, no fixed row heights.
- Cell margins: approximately 0.06-0.08 in.
- Scope, role, and feature matrices reuse the source thin-grid table pattern with gray header fill.

## Components

- Cover: pale-blue vertical band at left; centered title; client label/logo/name; implementer label/logo/name.
- Body header: four-cell bordered strip containing implementer logo, client logo, document title, and system label.
- Body footer: two-cell document-name/page strip plus red copyright lead and confidentiality statement.
- Major section: black full-width heading band with white text.
- Subsections: bold numbered headings without colored blocks.
- Legend: concise mapping for Standard, Manual, Customization, and Integration.
- Process section: short purpose paragraph followed by activity table. Flow diagrams may be added in a later revision; this draft prioritizes approved business-process tables.

## Content Flow and Slot Map

1. Cover - rewrite title, client identity, version, and date; replace client logo with MITO logo; preserve implementer identity pattern.
2. Document Control - rewrite history and distribution tables.
3. Approval - create draft approval roles for MITO and implementation team; leave names/signatures blank where not provided.
4. Legend - rewrite Type definitions and architecture boundary in Indonesian.
5. Table of Contents - static draft TOC; page numbers may refresh in Word.
6. Project Overview - rewrite overview, objectives, scope, architecture, roles, and design principles.
7. Feature Overview - create the SFA mobile feature matrix from the current feature draft.
8. Business Processes - create P01-P18 process sections in Indonesian using the approved five-column activity format.
9. Decisions and Open Items - capture confirmed decisions and clearly label low-priority/provisional items.
10. Appendix - include status glossary and traceability summary when useful.

## Stable Locators and Rewrite Policy

- Editable body location: `word/document.xml` body content. It will be replaced because this is a new blueprint, while source styles and page system remain authoritative.
- Editable headers/footers: `word/header*.xml` and `word/footer*.xml`; preserve the source four-cell header and two-cell footer patterns while rewriting logos and text.
- Preserve-only: theme, styles, numbering definitions, package properties required by Word, and the implementer logo asset.
- Replace: Forecastle logo/name and all Port Agency content.
- Add: MITO logo converted from the supplied SVG for Word compatibility.
- Remove from visible content: Odoo 16/Port Agency references not applicable to the SFA Mobile scope.

## Package Preservation

- Source package inventory: 100 parts, including styles, numbering, theme, headers, footers, 67+ media items, and field relationships.
- Preserve `word/styles.xml`, `word/numbering.xml`, `word/theme/theme1.xml`, document settings, and core relationships unless a new relationship is required for MITO logo or page fields.
- Existing Port Agency body images are not reused. Orphaned source media may remain in the working package to avoid unintended package loss; they must not appear in rendered content.
- Header/footer relationships may change only to replace the client identity and update document text.

## Fidelity Gates

- Reference remains byte-for-byte unchanged at the recorded SHA-256.
- Final document remains A4 portrait with the same margin and recurring header/footer visual pattern.
- MITO logo appears proportionally correct and is not stretched.
- Major-section black bands, heading hierarchy, table borders, gray headers, and footer furniture remain recognizably source-derived.
- No Notes column appears in process tables.
- Tables repeat headers and split cleanly without clipped text or fixed-height rows.
- No Forecastle or Port Agency visible content remains.
- Final render must be visually inspected page by page using Microsoft Word export when LibreOffice is unavailable.
