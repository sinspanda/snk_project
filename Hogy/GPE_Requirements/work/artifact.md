# Execution contract - HOGY blueprint format for GPE

## Reference and evidence

- Retained reference: `E:\Panda\Hogy\Blueprint_NSI HOGY_Payroll System V1.0.docx`.
- SHA-256: `23f9245e6620f7b8f75cb4866d93bfb9ecb3f19c4c89715cb73c1ac1c2f8eb4d`.
- Supplemental outline inspection only: `Blueprint_NSI%20HOGY_Payroll%20System_Draft%20Content%20V1.0.docx`; its project requirements, roles, formulas, counts and D365FO classifications are NOT GPE source data.
- Complete ZIP part sizes and hashes: `reference_inventory.json` in this folder.
- Section, field, image and footnote packaged audits executed; XML inspected for all 153 body blocks and all headers/footers. Cover images extracted and visually inspected.
- Reference render attempted to `template-reference-render`; failed because soffice is unavailable. Rendered page count and visual page fidelity are unverified. Use structural fallback allowed by documents skill; disclose at delivery.
- Authoritative GPE content: `requirements.md`. Reference controls formatting, not business facts.

## Page system

Two portrait sections, both new-page, no different-first-page flag. Preserve both sectPr byte-equivalent subtrees.

Section 1 cover: width 11894, height 16834 DXA; margins top/bottom/right 1138, left 1411; header 734, footer 677; columns gap 720; docGrid linePitch 272. Header rId10; default footer rId12; dormant even footer rId11.

Section 2 body: width 12240, height 15840 DXA; margins top/bottom 1440, left 1800, right 1041; header/footer 720; columns gap 720; docGrid linePitch 360. Header rId17; default footer rId18. Usable body width 9399 DXA; source activity grid 9425 (26 DXA wider), preserve template geometry rather than apply generic preset.

## Typography and paragraphs

- Preserve `word/styles.xml`, `word/numbering.xml`, theme, fontTable and webSettings byte-for-byte. Resolve styles by cloning source paragraph pPr/rPr, not rebuilding a generic document.
- Normal: Arial ascii/hAnsi, line 360 auto; actual run sizes may inherit. Source body block 77 has firstLine 720, and a source run with cs Arial. Clone this paragraph for body text; no new font/size system.
- BP Head 1 (BPHead1): based on Heading1; size 40 half-points, before/after 120, line 240, justified, source shade; multi-level numId53. Frontmatter clone block46 suppresses numbering with numId0. Chapter heading clone75 uses num53.
- BP Head 2: Arial through Normal, size28 half-points, line240, after120; left/hanging431; num53 level1, outline1. Clone block76.
- BP Head 3: size24 half-points, before/after120; left/hanging851; num53 level2, outline2. Clone block133.
- List Paragraph: real numbering inherited numId3; before/after120, justified. Clone block84 and replace text; retain list numbering.
- Cover top: Cambria24pt centered; main title Cambria24pt centered with line480; Module Series label14pt; module value16pt line276.
- Cover prepared labels: Cambria9pt blue0070C0; organization15pt black. Preserve textbox coordinates and paragraph roles. Do not make up company full name or authorship.
- Tables: source activity header/body Arial9pt, line240; header bold white, fill002060, centered; body black, vertical center; borders single4 auto. Source activity grid `[1513,1477,1198,2483,1607,1147]`, width9425. Clone row patterns. Repeating header added as safe table-continuation behavior; row minimum heights removed only in cloned content to avoid padding/capacity problems; no exact heights introduced.
- Compact matrix patterns: source 2-column scope table grid2065/6397 and source 3-column addon table; preserve their source geometry and cell paragraph styling.
- Document-control tables: gray595959 header, white text; light gray BFBFBF single4 borders, source indent108. Preserve original table/column sizes and replace rows as needed.

## Components and flow

Preserve cover shape/sidebar layout and cover/body section break. Frontmatter contains Document Control (history/distribution), Approval (client and implementor), Table of Contents, Legend. Main chapters: Project Overview; Master Data dan Konfigurasi; Report dan Printout; Alur Proses; FitGap Traceability dan Open Decisions. Extend subsection slots using cloned H2/H3 and tables for GPE's broader GA/Finance requirements.

Header retains its four-cell frame, title SYSTEM BLUEPRINT and original geometry. Logo slots become text HRIS/GPE/ODOO because source HOGY, NSI and Dynamics identities are not GPE-provided branding. Footer retains structure/page field, but project title/confidentiality text becomes GPE draft metadata. Page fields are retained and marked dirty.

## Slot map (zero-based body block indexes in retained source)

- document.xml body0: cover platform text in both AlternateContent branches -> ODOO; preserve shapes.
- body4: title/series -> System Blueprint / Module Series / HRIS, People & Payroll.
- body16: prepared-for name -> GPE; remove HOGY logo drawings inside textbox only, retain outer anchor and text geometry.
- body31: stray `aaa` text -> empty, retain decorative shape.
- body34: prepared-by identity -> Draft untuk Review; remove NSI logo drawings, preserve outer textbox.
- body45: cover/body section properties preserve.
- body46-74: frontmatter layouts preserve; history/distribution and approval tables rewritten. Approval wording explicitly excludes OPEN items from implicit approval. Old reviewer names removed; signatures remain blank.
- body67: TOC doc-part SDT and sdtPr retained. Update cached field content with links to actual new headings; suppress page numbers in cached TOC (no guessed pagination). Keep live TOC field and set updateFields in settings. Word can refresh layout-dependent fields.
- body70: Legend followed by status and fit-gap interpretation using cloned table pattern. Remove obsolete OLE diagrams in frontmatter; they are QC/source content, not GPE requirements.
- body75-end before final sectPr: replace all old Port Agency, bank Mandiri, production/QC and HOGY requirements with GPE material. Use source heading/list/body/table components, extending repeated patterns to fit content. Activity matrix keeps six columns: Activity ID, Activity Name, PIC, Description, Solution, Comments / Notes. Descriptions are short; full remaining rules and criteria follow as full-width paragraphs to prevent giant table cells.
- header2.xml: replace three logo slots with plain identity text; keep header title/frame.
- footer3.xml: replace stale project name and copyright/author claim with GPE internal-draft notice; preserve page field.
- docProps/core.xml/app.xml: update title/subject and clear old authors, client details and stale document statistics.

## Package preservation and allowed differences

Preserve every part not listed as editable/removable, including styles, numbering, theme, fontTable, webSettings, customXml and its relationships, root relationships, footnotes/endnotes and unused blank cover header/footer parts. Preserve unchanged source header/footer geometry.

Editable: document.xml, header2.xml, footer3.xml, settings.xml, document/header2 relationships, Content_Types, core/app properties.

Remove from output only: all five source branding/QC media assets and both OLE objects, and their obsolete relationships/content type overrides. Source originals remain intact. New user requested client-specific content and branding replacement justify these differences; no raster assets are generated or altered.

## Fidelity gates

Source SHA stays unchanged. Exactly two sections with identical geometry and relationship IDs. Source style/numbering/theme hashes unchanged. All preserve-only parts identical. All 43 functional IDs, 4 NFRs, 7 INTs, 8 RPTs, 14 UATs and 16 decisions retained. Activity IDs map back to requirement IDs; all criteria present. No HOGY, Port Agency, D365FO, bank Mandiri, QC/production, old named reviewer, logo or embedded source content leaks into GPE output. No guessed standard/custom classification or approvals. TOC/bookmarks/fields and relationship targets structurally valid. Final render attempted; lack of soffice means visual QA cannot be claimed.
