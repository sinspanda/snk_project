# MESA — Technical Implementation Plan: Grade Change Requests

Target: Odoo 18 Enterprise, Inventory · CR v0.1 · Commercial effort: 2 mandays.

Build an Inventory feature that records a grade change request, lets an Inventory Approver validate it, and applies the new grade to the selected product masters on its Effective Date. One request has one date, one new grade, one mode, and one or more product lines.

- [Change Request Pengajuan Perubahan Grade](https://chatgpt.com/library?file_id=libfile_32d809b75e0c81918e494fc966cbea76&account_id=personal)

The workflow, screen behavior, and roadmap are specified in this file. No image attachment is required to implement the feature.

## 1. Start here — coding agent instructions

1. Read the target repository's AGENTS.md. Locate the existing MESA Inventory/Product add-on, its manifest, test conventions, and security patterns. The custom source was unavailable when this plan was written. Identifiers in this document are proposed unless explicitly marked as standard product models.
2. Trace the actual grade fields on `product.template` and `product.product`. Record their field names, types, comodel or selection values, where each value is stored, and existing write hooks. Inspect at least one template with two variants in a development database. Search for `grade`, `snk_grade`, product model extensions, existing security groups, and scheduled actions. A field visible on a variant may still write to shared template storage. The request model names in section 3 are final.
3. Identify the real Inventory User group XML ID, the company or record scope already used by MESA, the existing product picker behavior, and the project's sequence and scheduler patterns. Reuse those patterns. Propose a new add-on only if that fits the repository conventions.
4. Implement the settled parts in sections 2–6. Keep grade lookup, target resolution, and application in a small service or model methods so the field mapping and policy can be reviewed separately. Treat section 7 as business decisions to confirm. Keep affected behavior out of production until confirmed. If Variant mode cannot isolate one SKU with the existing grade model, report the gap before changing product schema.
5. Work in development/UAT. The handoff must list actual models and grade fields used, unresolved decisions, files changed, tests run, and deployment steps.

## 2. Scope and lifecycle

| Actor | Allowed action |
| --- | --- |
| Inventory User | Open the menu, create and edit a Draft, save it, discard unsaved form changes, and duplicate a request they can read, subject to create access. |
| Inventory Approver | Inherit Inventory User access through the new group's implied group. Review a saved Draft and click Validate. |
| Scheduled Action | Apply the grade through a private server-side path and set Applied At on success. Cancel overdue Validated requests that have not been applied. Use the narrow privileges required by the project. |

- States: `draft`, `validated`, and `canceled`. A new request starts in Draft. Only the Validate action can transition a saved Draft to Validated. The Scheduled Action transitions overdue, unapplied Validated requests to Canceled.
- After Validate, the business fields and lines are read-only. Status stays Validated after successful application. Applied At distinguishes waiting requests from requests that have been applied. Canceled requests remain read-only and can be duplicated into a new Draft.
- Scope covers the grade on product masters and the request history. Stock moves, lots, valuation, accounting, pricelists, and historical transaction grades/reports are outside this CR.

### End-to-end workflow

1. **Inventory User creates a Draft.** Enter Effective Date, New Grade, and Mode in the header. Add product lines by selecting either Product Template directly or Product Variant directly, according to the selected mode. The system reads Current Grade from the selected product master.
2. **Inventory User saves the Draft.** Save checks Effective Date against H+1 in WIB, required data, target type, duplicates within the request, and same-mode overlap across requests on the same Effective Date. If a check fails, reject the save and show the reason. After correction, the user can Save again. A successful Save stores the lines and their Current Grade snapshots.
3. **Inventory Approver reviews and clicks Validate.** The system checks the group and saved Draft data, records who validated it and when, sets Validated, and locks the header and lines. The H+1 date check belongs to Save. Product grades change through the Scheduled Action.
4. **The daily Scheduled Action evaluates requests.** It uses the run's date in Asia/Jakarta and follows the decision table below.
5. **Inventory User duplicates a Canceled request when a replacement is needed.** Enter a new Effective Date, copy the business header and every product line to a new Draft, and reread and store Current Grade on each new line. The old request keeps its original history. The new Draft goes through Save and Validate independently.

| State and condition at Scheduled Action run | Outcome |
| --- | --- |
| Validated, Applied At empty, Effective Date equals run date | Apply New Grade. For overlapping Template and Variant requests, apply Template first, then Variant. On success, fill Applied At and keep Validated. |
| Validated, Applied At empty, Effective Date before run date | Set Canceled and record cancellation reason and time. Skip product updates. |
| Validated, Applied At empty, Effective Date after run date | Leave the request queued for its Effective Date. |
| Validated with Applied At filled, Draft, or Canceled | Leave the request as is. |

If an application fails, roll back that request's product changes and leave Applied At empty. An overlapping Variant waits while its Template request is still unapplied. Other eligible requests can continue.

## 3. Proposed models and UI

Final model names: header `snk.grade.request`, line `snk.grade.request.line`. Field names below are proposed unless already present in the repository.

| Model | Proposed field | Requirement |
| --- | --- | --- |
| Request | `name` | Read-only request number. Use a sequence, e.g. `GCR/2026/00001`. |
| Request | `effective_date` | Required Date, interpreted in Asia/Jakarta. One value for every line. |
| Request | `new_grade_id` or `new_grade` | Required. Use the existing master grade definition and its actual field type. |
| Request | `mode` | Required selection. Values `template` / `variant`. Labels By Product Template / By Product Variant. |
| Request | `state`, `line_ids` | Read-only workflow state and One2many product lines. |
| Request | `validated_by_id`, `validated_at`, `applied_at` | Server-controlled audit fields. Applied At is actual execution time, displayed in the user's time zone. |
| Request | `canceled_at`, `cancel_reason` | Server-controlled audit fields. For automatic cancellation, record the time and reason that the Effective Date passed without application. |
| Request | `source_request_id` | Proposed read-only link to the request copied by Duplicate, for tracing a replacement back to the original. |
| Line | `request_id` | Required parent. Prevent direct edits, reparenting, or deletion from bypassing parent state checks. |
| Line | `product_tmpl_id` | Editable target in Template mode. In Variant mode, show the variant's template as a derived read-only value. |
| Line | `product_id` | Editable target in Variant mode. Hide in Template mode. |
| Line | `current_grade` | Stored, read-only grade snapshot from the actual selected template or SKU. Capture it when a target is selected or changed and saved, including when Duplicate creates a new line. Retain it for an unchanged target and preserve it after Validate, Apply, or Cancel. Use the actual master grade type. |

Menu: Inventory → Grade Change Requests, placed under the appropriate existing menu branch after repo discovery. List shows number, Effective Date, New Grade, Mode, Status, and Applied At. Form has the header and a Products tab.

- **By Product Template:** Add a line → search and select Product Template directly. Hide Product Variant. Show Current Grade.
- **By Product Variant:** Add a line → search Product Variant directly by SKU or name. Derive Product Template from that variant. Show Current Grade for the variant. Template selection is unnecessary.
- **Draft:** Editable header inputs and the active product selector display in bold with an underline using standard Odoo controls where possible. System-derived fields remain read-only. Use native Save/Discard icons. Show Validate only to Inventory Approver on a saved Draft.
- **Validated and Canceled:** Display all fields and lines read-only. Hide Validate and line add/delete actions. Include Canceled in the statusbar and list/search filters. Allow Duplicate subject to normal read and create access.
- Proposed UX guard: require removing existing lines before switching mode. This avoids silently clearing selections or retaining targets from the wrong mode.

### Duplicate and grade history

1. Duplicate copies the business header (New Grade and Mode) and all selected product lines into a new Draft. Use a new sequence number and new line records. Keep the source request and its lines intact.
2. Ask for the new Effective Date before persisting the duplicate, for example with a Duplicate wizard if the native action cannot collect the date first. Do not carry forward the source date. Apply the normal H+1, required-field, and same-mode overlap checks to the new request.
3. Re-read the grade from the current product master for every copied line. Save it as the new line's Current Grade snapshot. The source line keeps its original snapshot. For example, if the source captured Grade A and the master now has Grade B, the new Draft records Grade B while the source still shows Grade A.
4. Reset validation, application, and cancellation audit fields on the new record. It must go through Validate again. The scheduler does not automatically create replacement requests.

## 4. Validation and security contract

| ID | Trigger | Required behavior |
| --- | --- | --- |
| VAL-01 | Save Draft | Require Effective Date ≥ tomorrow, using the server-calculated current calendar date in Asia/Jakarta. Reject today and past dates with “Effective Date minimal besok (H+1, WIB).” |
| VAL-02 | Save and Validate | Require date, new grade, mode, and at least one complete line. Require the target type matching Mode. Reject duplicate template IDs in Template mode or duplicate variant IDs in Variant mode. Two different SKUs from one template are valid in Variant mode. |
| VAL-03 | Validate | Check approver group and Draft state server-side. Verify the persisted form and record validator/time. Do not rerun the H+1 rule in Validate. |
| VAL-04 | Validated or Canceled | Block manual edits to business/audit fields and block line mutations and deletion. Enforce on server paths including import and RPC. Client visibility is for UX. |
| VAL-05 | Scheduler | Eligible only when Validated, Effective Date equals today's date in WIB, and Applied At is empty. |
| VAL-06 | Scheduler | Update all targets of a request and set Applied At atomically. On failure, roll back that request's product changes, leave Applied At empty, and log the error. Continue processing other eligible requests. |
| VAL-07 | Save Draft | Reject overlap across requests with the same Effective Date and Mode. Compare Product Template IDs in Template mode and Product Variant IDs in Variant mode. Exclude the request being edited. Template/Variant overlap is allowed. |
| VAL-08 | Scheduler | For overlapping Template and Variant requests on the same Effective Date, apply Template first, then Variant. The explicit Variant request sets the final grade for its selected SKU. |
| VAL-09 | Scheduled Action | For Validated requests with Effective Date before today in WIB and blank Applied At, set Canceled and record the reason and timestamp. This branch performs no product grade writes. |
| VAL-10 | Duplicate | Copy the header and target lines to a new Draft using a new valid Effective Date. Pull and store fresh grade snapshots, reset audit fields, and run the normal Save checks. |

Implementation notes:

- Calculate WIB explicitly in a shared date helper. Inject or patch its clock in tests. H+1 means **next calendar day**, including weekends. Saving at 23:50 WIB on 5 Nov accepts 6 Nov. Saving after 00:00 WIB on 6 Nov requires at least 7 Nov.
- Apply the Save rules to actual user-edit persistence, including create, import, and ordinary Draft writes. Validate the final header/line state after One2many edits, so intermediate command steps do not falsely fail. Prevent direct line operations from bypassing equivalent rules. Use the project's ORM conventions for batched create and write.
- For VAL-07, compare the resulting target set with other saved requests for the same date and mode. Use Draft and Validated, including already-applied requests, as the proposed comparison scope. Exclude Canceled requests from reservations. Compare within the same actual grade-write scope. A shared grade field must not be treated as company-specific. The same target on different dates is valid. Report the conflicting target, date, mode, and existing request number when visible to the caller.
- Make the same-mode Save check atomic against concurrent saves. Use a database uniqueness rule for a canonical reservation key or a transaction lock plus recheck. The key must include the effective date, mode, target ID, and grade-write scope if applicable. Cover parent edits, direct line writes, and bulk imports. Validate does not reject cross-mode overlap.
- Keep Validate and Scheduled Action updates on controlled server paths so routine Draft-save validation does not fire during a state change, application, or cancellation. Reject forged state/audit values and grade snapshots from ordinary create/write. Do not trust a caller-supplied context flag to bypass access or state checks.
- Scope record access using existing MESA conventions. Enforce group membership on the server action as well as on the button. Do not use unrestricted privilege escalation on user-facing actions.

## 5. Daily Scheduled Action contract

Register an Odoo Scheduled Action (`ir.cron`) calling a private method on `snk.grade.request`. Configure it to run daily. The functional owner can set the execution time. Capture the run's business date once in Asia/Jakarta and use that date for both branches. Validate does not trigger the Scheduled Action. A request validated after the day's run can only apply if a further run takes place that same WIB date.

```text
today = current calendar date in Asia/Jakarta
overdue = requests with state=validated, effective_date<today, applied_at empty
for each overdue request:
    acquire concurrency guard and re-read overdue eligibility
    if still overdue and unapplied: set Canceled and record reason/time

candidates = requests with state=validated, effective_date=today, applied_at empty
for mode in [template, variant]:
    for each eligible request of this mode in stable order:
        begin isolated transaction scope for this request
        acquire concurrency guards and re-read eligibility and dependencies
        if no longer eligible: skip
        if mode=variant and an overlapping Validated Template is unapplied:
            defer this Variant request
        resolve distinct targets from Mode and saved lines
        verify the new grade and all targets can still be written
        update actual grade storage through the existing ORM path
        set Applied At to the actual successful execution time
        on error: roll back this request and log request ID, mode, and failure
```

- **Template mode:** resolve each selected template to its grade storage. Confirm the effect on underlying variants before enabling writes.
- **Variant mode:** update the selected SKU's own grade. Prove with a sibling SKU test that the operation does not update a shared template field.
- **Cross-mode precedence:** for example, Template A → Grade B and Variant A-01 → Grade C on the same date. Apply the template request first, then set A-01 to Grade C. Determine dependencies from the selected SKU's parent template. If an overlapping Template application fails or is still pending in another batch, defer its dependent Variant request. Continue with unrelated requests.
- Make repeat runs and overlapping invocations safe. Use a scheduler-level or overlapping-target guard in addition to any per-request guard so separate workers and bounded batches cannot reverse Template → Variant ordering. Recheck Applied At and dependency state under the guard. Commit grade writes and Applied At together.
- **Late Template validation:** a same-day Template can become Validated after its overlapping Variant was already applied in an earlier run. Proposed guard: do not apply the late Template automatically if it could overwrite the Variant result. Log both request IDs and route for review. Confirm this handling before release, including whether a coordinated Template → Variant replay should be supported.
- A manual rerun on the same WIB date can retry a failed application while Applied At is empty. If the date has passed, the next run cancels the request. To proceed, a user duplicates the request and enters a new Effective Date.
- Keep cancellation and application mutually exclusive. Recheck state, date eligibility, and Applied At under the same per-request guard used for application. An already-applied request remains Validated, even on later days.

## 6. Delivery order and acceptance tests

1. **Discovery:** document grade fields, actual write effects, security group XML IDs, and assumptions for section 7.
2. **Data and access:** add models, sequence, state guards, group inheritance, ACLs, and view/menu actions.
3. **Form and validation:** build conditional product selectors, Save checks, duplicate guards, and the Validate action with audit trail.
4. **Application and recovery:** add the daily Scheduled Action, real target mapping, isolated failure handling, overdue cancellation, and Duplicate with new-date entry and fresh grade snapshots.
5. **SIT and handoff:** update the module on UAT, verify permissions with both roles, test the scheduler before production enablement, and capture evidence.

| Test | Setup and expected result |
| --- | --- |
| T01 — WIB boundary | On 5 Nov at 23:50 WIB, Save rejects 4/5 Nov and accepts 6 Nov with valid data. At 00:00 WIB on 6 Nov, minimum advances to 7 Nov. |
| T02 — Required data | Missing grade, mode, date, product, mismatched target, or duplicate target fails. Distinct variants under the same template can coexist. |
| T03 — Mode behavior | Template selects a template directly with Variant hidden. Variant selects by SKU with template derived. Discard reverts unsaved input. |
| T04 — Role and lock | User can save Draft but cannot Validate by UI or RPC. Approver can create and Validate. Attempted header or line mutation and request deletion after Validate are rejected. |
| T05 — Validate and date | An unchanged Draft saved the previous day with today's Effective Date can be validated today, assuming valid data. Grade changes only when scheduler runs. |
| T06 — Scheduler filter | Only Validated requests due on the run's WIB date with blank Applied At are applied. Draft, future, Canceled, and already-applied requests are skipped. Overdue, unapplied Validated requests enter cancellation only. |
| T07 — Target isolation | Variant mode updates only the selected SKU, leaving its sibling unaffected. Template mode follows the confirmed behavior for variant grades. |
| T08 — Retry and atomicity | Forced failure on a later target rolls back earlier updates and leaves Applied At empty. Another valid request can still apply. A successful rerun or overlapping run does not reapply a completed request. |
| T09 — Audit | Validator and time are recorded on Validate. Applied At appears only after success. Stored Current Grade remains the captured grade when the product master changes later. |
| T10 — Same-mode overlap on Save | Two Template requests for the same template/date are rejected on the second Save. Repeat for the same SKU in Variant mode. Saving an unchanged request does not conflict with itself. Different dates and different SKUs of one template are accepted. Test concurrent Save and import paths. |
| T11 — Cross-mode precedence | Save and Validate both requests for Template A → Grade B and A-01 → Grade C on the same date, including reverse creation order. Scheduler applies Template first. Final grade of A-01 is C. Verify ordering across batch boundaries and overlapping scheduler invocations. |
| T12 — Template dependency fails | A failed overlapping Template request leaves its dependent Variant unapplied. Unrelated requests can proceed. After a successful same-day retry, the Template applies before the dependent Variant. |
| T13 — Overdue cancellation | A request due 10 Nov remains unapplied when the action runs on 11 Nov WIB. It becomes Canceled, records reason and time, retains its lines and snapshots, and leaves product grades and Applied At untouched. An applied request for the same prior date stays Validated. |
| T14 — Duplicate and refresh | Duplicate a Canceled request with multiple lines after changing a product's master grade. With a valid new date, the copy has a new number, Draft status, copied mode/new grade/targets, fresh stored grade snapshots, and empty audit fields. The source remains unchanged. An invalid date or same-mode conflict prevents creation. |
| T15 — Daily timing | Run the action in the morning, then validate an otherwise eligible request later that day. It is applied only if the action runs again on that same WIB date. Otherwise, the next daily run cancels it. |

Roadmap baseline: assessment 4 Nov 2026 · CR and handover 5–6 Nov · development 9–13 Nov · SIT 16–17 Nov · UAT 18–19 Nov · target go-live 20 Nov after UAT acceptance.

## 7. Decisions to confirm before release

| Decision | Suggested starting point |
| --- | --- |
| Template propagation | Template → Variant precedence is confirmed for overlapping requests. Confirm what the Template write does to existing variant-specific grades for SKUs without an explicit overlapping Variant request. Verify the actual grade storage before coding propagation. |
| Overlap edge cases | Confirm which saved states reserve same-mode targets at Save. Proposed scope is Draft and Validated, including applied. Confirm handling for a late Template validation after an overlapping Variant already applied. The normal Template → Variant ordering is settled. |

Definition of done: one reviewable change set with verified grade field mapping, server-side Save checks for same-mode overlap, role restrictions, two-mode UI, daily Scheduled Action with ordered and atomic application and overdue cancellation, Duplicate with stored grade history, and SIT/UAT evidence. Record agreed answers to the remaining decisions before production enablement.
