# MITO SFA Mobile - Feature Design Draft

**Version:** 0.3  
**Status:** Working Draft - For Internal Review  
**Scope:** SFA Mobile Application  
**Architecture Boundary:** SFA Mobile communicates only with CMS. CMS communicates bidirectionally with Odoo.

## 1. Design Principles

- Registered and active internal and external users can log in according to their assigned roles.
- SFA Mobile does not communicate directly with Odoo.
- The mobile offline database is a device-local cache and pending-transaction queue.
- The mobile offline database is not the authoritative business database.
- Approval-matrix configuration is maintained in CMS as the authoritative source.
- Master-data configuration remains in CMS for minimum implementation effort.
- Internal and external users use one SFA Mobile application with role-based menus, data access, and actions.

## 2. Proposed Mobile Roles

| Role Group | Proposed Roles | Description |
|---|---|---|
| Internal | Sales | • Customer visit; • Customer and prospect; • Order; • Invoice collection submission; • Assigned partner review |
| Internal | Sales Manager | • Team monitoring; • Notification; • Selected mobile approval |
| Internal | Promotor / SPG | • Assigned outlet activity; • IMEI registration; • Product and order support; • Collection evidence when permitted |
| Internal | GTM (Go To Market) | • Prospect registration; • Assigned customer follow-up; • Customer and prospect information according to access |
| External | Dealer Owner | • Partner profile; • Partner staff; • IMEI and reward; • Quotation request |
| External | Dealer Staff | • IMEI registration; • Quotation request; • Reward activity according to access |
| External | Distributor / Retail Partner | • Partner self-service according to assigned role |

## 3. Common and Internal Sales Features

| ID | Module | Description | Users | Position |
|---|---|---|---|---|
| SFA-01 | Login & Access | • Common login for registered and active internal/external users; • NIP, email, phone, or approved identifier; • Password login; • Forgot password; • Account activation status; • Role-based menu; • Session management; • Logout | All registered users | Enhance |
| SFA-02 | Dashboard | • Actual visit summary; • Actual order summary; • Actual revenue summary when available from CMS; • Completed Visit with Order; • Completed Visit without Order; • Visit-to-Order Conversion; • Today's activities; • Pending activities; • Out of Stock outlet summary; • Low Stock outlet summary; • On Stock outlet summary; • Stock Opname Due summary; • Quick action to open outlet detail or schedule a visit; • Integration Staging limited to Super Admin; • Pending, Synced, and Failed integration records; • Customer-level annual/monthly target excluded from minimum scope; • Optional simple monthly sales-user target maintained in CMS; • Lower priority for the current implementation draft | Sales, Sales Manager, Super Admin | New |
| SFA-03 | Customer & Prospect | • Prospect registration by Sales, Promotor, or GTM; • Mandatory Salesperson assignment; • Business segment such as Retail, Pareto, or another CMS-defined segment; • Prospect is stored only in CMS; • Sales, Promotor, or GTM performs manual commercial follow-up; • Assigned Salesperson confirms the deal through SFA; • CMS updates the same record's status/type from Prospect to Customer; • No duplicate Prospect and Customer master data; • Salesperson and segmentation remain linked; • Only Customer data is integrated from CMS to Odoo | Sales, Promotor / SPG, GTM | Enhance |
| SFA-04 | Visit Planning | • Agenda view; • Date-strip navigation; • Daily visit list; • Customer assignment; • Add visit; • Submit reschedule request with proposed date/time and reason; • Schedule field is replaced only after reschedule approval; • Approved reschedule replaces the current planned date/time with the proposed date/time; • Rejected reschedule leaves the current planned date/time unchanged; • Schedule Detail contains a Reschedule History tab/section; • Reschedule History stores previous date/time, proposed date/time, reason, requester, approver, status, and timestamp; • Reminder; • Full monthly calendar deferred from minimum scope | Sales | Enhance |
| SFA-05 | Visit Execution | • GPS check-in/out; • Actual check-in/out timestamps always follow the device/server transaction timestamp; • Radius validation uses the assigned customer/dealer/outlet location; • User can visit and clock in on the proposed reschedule date while approval is still pending; • If reschedule is approved after clock-in, the planned schedule is replaced by the approved proposed date/time while actual timestamps remain unchanged; • If reschedule is rejected, the current planned schedule remains unchanged while actual timestamps still record the completed visit; • Distance verification; • Visit-evidence photo; • Task list; • Notes; • Visit outcome; • No-order reason; • Complaint/follow-up indicator; • Visit-to-order link; • Optional outlet stock opname task; • Offline pending synchronization | Sales | Enhance |
| SFA-06 | Product Catalog & MITO Stock | • Product catalog; • Product image, code, category, and brand; • Product and price context returned by CMS; • Customer commercial context may include pricelist, product assortment, territory, and default fulfillment warehouse; • One default warehouse is proposed per customer/territory for minimum scope; • Permitted warehouse selector when the user can transact from more than one warehouse; • Stock displayed per selected warehouse; • Do not aggregate multiple warehouses into one stock figure unless explicitly agreed; • MITO available stock received through CMS; • Search, filter, and barcode scan; • If no customer-specific assortment exists, display all permitted saleable products | Sales, Promotor / SPG, External Partner | Enhance |
| SFA-07 | Quick Order | • Select one customer; • Browse/search catalog; • Add multiple products to cart; • Adjust quantity; • Display price from CMS commercial context; • Display discount and tax values according to CMS rules; • Detailed discount and tax design remains open for a dedicated discussion; • Review cart; • Save draft; • Confirm one cart as one Sales Order / Quotation; • Submit through CMS; • Link to visit when applicable | Sales | New |
| SFA-08 | Sales Order | • Order list and detail; • Customer and product lines; • Quantity, price, and amount; • Status and timeline; • Edit/cancel draft according to access; • Submit order; • Approval status; • Rejection reason | Sales, Sales Manager | Enhance |
| SFA-09 | Sales Tracking | • Dashboard aggregate with list drill-down; • Sell-In and Sell-Out tabs; • Summary by customer; • Summary by product; • Period filter; • Order history; • Order created from Visit Detail automatically stores visit_id; • Converted Visit = Completed Visit with at least one linked Sales Order; • Non-Converted Visit = Completed Visit without a linked Sales Order; • Multiple orders from one visit count as one Converted Visit; • Cancelled, Missed, and Rescheduled visits are excluded; • Visit-to-Order Conversion = Converted Visit / Total Completed Visit x 100%; • No-order outcome/reason is required for Non-Converted Visit | Sales, Sales Manager | Enhance |
| SFA-10 | Outlet Stock Movement & Opname | • Lightweight stock ledger per outlet and product; • CMS stores On Hand as the authoritative outlet-stock quantity; • Stock Receipt creates an IN movement; • Draft receipt flow: select a known delivery/order reference and confirm received quantity; • Manual product, quantity, date, and reference entry is available when no delivery reference exists; • Standard delivery reference can only be confirmed once; • Partial receipt is entered as Manual Receipt using a unique derived reference, for example DO-001-PARTIAL-1; • Derived partial reference can retain the same parent delivery reference for traceability; • Each full manual/partial reference must be unique; • Receipt flow is accepted for the feature draft and will be reviewed again during process-flow design; • Sell-Out creates an OUT movement; • For IMEI products, approved Warranty Activation / Sell-Out Registration automatically creates the OUT movement; • Reward Claim does not create a second stock OUT movement; • Stock Opname displays System On Hand and accepts Counted Quantity; • Adjustment Quantity = Counted Quantity - System On Hand; • Positive difference creates Adjustment IN; • Negative difference creates Adjustment OUT; • After posting the adjustment, On Hand equals Counted Quantity; • Do not replace or delete earlier movements; preserve movement history for audit; • Dealer Staff can record receipt, sell-out, and self-opname for its own outlet; • Assigned Sales / SPG can record receipt or perform opname during a visit; • Display On Hand and last-opname date; • No stock-aging or freshness classification in minimum scope; • Buffer stock is configured per product in CMS; • Out of Stock when On Hand is zero or below; • Low Stock when On Hand is above zero and at or below product buffer; • On Stock when On Hand is above product buffer; • Opname frequency is configured in CMS; • Next Opname Due = last-opname date + configured frequency; • Completing an opname recalculates the next due date; • Opname Due creates a dashboard alert and one-click Schedule Visit action; • Do not automatically create a visit to avoid unwanted schedules; • Feature is available from Customer Detail and Visit task; no standalone stock menu is required | Dealer Staff, Assigned Sales / SPG | Simplify |
| SFA-11 | Order Billing & Collection | • Orders ready for invoice; • Invoice number and status; • Payment status and due date; • Download/share/print invoice PDF; • Collection submission: invoice, date, amount, method, reference, and mandatory attachment; • Collection can be captured offline; • When the user confirms the collection in SFA, the SFA invoice/payment status becomes Paid; • SFA does not display Odoo payment-sync status; • CMS creates the payment record and manages Pending Odoo Sync, Synced, or Sync Failed statuses; • No accounting-journal creation or journal configuration in SFA Mobile scope; • CMS-to-Odoo payment synchronization is handled later under CMS/Odoo integration scope | Sales, Promotor / SPG | Simplify |
| SFA-12 | Notification Inbox | • Standard in-app/push notification; • Unread indicator; • Mark as read; • Deep link to related record; • Visit, order, approval, invoice, sync, account, IMEI/reward, and system notification | All registered users | New |

## 4. External Partner Features

| ID | Module | Description | Users | Position |
|---|---|---|---|---|
| SFA-13 | Partner Registration | • Self-registration; • OTP/email verification; • Personal and business information; • Supporting-document upload; • Terms acceptance; • Submit registration; • Track approval/rejection; • Revise and resubmit; • Activate account after approval; • Login through SFA-01 after activation | External Partner | New |
| SFA-14 | Partner Profile | • Business and legal profile; • Address and outlet; • KTP, NIB, NPWP, and SIUP when required; • Every data change creates a review request; • Current approved data remains active during review; • Assigned internal Sales reviews changes; • Approved change replaces active data; • Rejected change displays reason | Dealer Owner | New |
| SFA-15 | Partner Staff | • Dealer Owner registers/invites staff; • Dealer Owner activates/deactivates staff; • View staff status; • No internal-Sales approval required; • Actions recorded in activity history | Dealer Owner | New |
| SFA-16 | Warranty Activation / Sell-Out Registration | • Represents dealer/outlet Sell-Out to the end customer; • Scan IMEI; • Manual IMEI entry as fallback; • Select product and Sell-Out date; • Capture minimum end-customer/warranty-holder information according to agreed privacy scope; • Upload invoice/attachment; • Select an eligible reward directly for the later claim; • No separate reward-program selection; • Submit warranty activation; • Approved activation changes warranty status to Active; • Approved activation creates Sell-Out record and outlet-stock OUT movement; • Active warranty makes the IMEI eligible for Reward Claim; • Local format validation; • Final validation by CMS; • Validate product, duplicate IMEI/Sell-Out, reward eligibility, reward availability, and warranty eligibility; • Offline Confirm creates Pending Sync; final CMS validation occurs after synchronization | Dealer Owner, Dealer Staff, Assigned SPG | New |
| SFA-17 | IMEI, Warranty & Reward History | • History scoped by dealer/customer; • Access according to role and assignment; • Display IMEI, product, selected reward, submitter, and Sell-Out date; • Display warranty status separately from reward-claim status; • Warranty status: Pending, Active, Rejected; • Reward Claim status: Eligible, Submitted, Approved, Rejected, Completed; • Rejection reason; • Permitted resubmission | Dealer Owner, Dealer Staff, Assigned Internal Sales | New |
| SFA-18 | Quotation | • External user-facing name is Quotation; • Represents dealer/outlet order to MITO as Sell-In; • Reuse the same catalog-cart-order concept as internal Sales Order; • Restricted external-partner access; • Select product and quantity; • Review cart; • Add notes/attachments; • Submit one cart as one Quotation; • Monitor status in the same record; • Cannot change restricted price, discount, tax, or approval; • Cannot access another partner's Quotation; • No separate Quotation Tracking module | External Partner | New |
| SFA-19 | Reward Catalog | • Display eligible rewards directly; • Reward name, image, description, and conditions; • Eligible products when applicable; • Availability when provided by CMS; • No separate program selection; • No point-balance mechanism in current scope; • Detailed reward eligibility, selection, approval, fulfillment, and exception flow is deferred until the other feature decisions are firm; • Reminder required before feature review is closed | External Partner | New |
| SFA-20 | Reward Claim | • Dealer/outlet selects an IMEI with Active warranty and Eligible reward status; • Selected reward is inherited from Warranty Activation / Sell-Out Registration and cannot be changed during claim; • No additional attachment is required; • No second manual review is required; • Offline Confirm creates Pending Sync; • CMS automatically validates that warranty is Active and IMEI has never been claimed; • If validation passes, CMS creates and locks the Reward Claim; • One IMEI has one Reward Claim and one reward; • Statuses: Eligible, Pending Sync, Claimed, Processing, Completed; • Claimed record is locked from mobile cancellation or duplicate claim; • Claimed monetary/dealer-payable reward instructs CMS to prepare Vendor Bill integration to Odoo; • Reward Claim does not create another Sell-Out or outlet-stock movement; • Detailed Vendor Bill mapping is discussed later under CMS/Odoo blueprint | External Partner | New |

## 5. Shared Mobile Capabilities

| ID | Module | Description |
|---|---|---|
| SFA-21 | Role-Based Experience | • Role-based menu and dashboard; • Role-based data and action access; • Customer/dealer limitation according to assignment |
| SFA-22 | Offline Mode | • Local cache for approved offline data; • Pending-transaction queue; • Offline indicator; • Read agreed cached data; • User can Confirm selected offline transactions; • Offline Confirm creates Pending Sync; • Supported: visit, queued order, Sell-Out/IMEI/warranty, stock receipt, Sell-Out, stock opname, collection, and partner quotation draft; • No final approval or duplicate validation while offline |
| SFA-23 | Synchronization | • Automatic/manual sync; • Last-sync timestamp; • Pending-sync count; • Transaction statuses: Pending, Synced, Failed; • Temporary connection/server errors remain Pending and auto-retry; • Failed is used for business validation or permission errors; • Failed record displays failure reason; • Edit & Resubmit is used when transaction data must be corrected; • Retry is used when the issue was resolved without changing transaction data; • Edit & Resubmit or Retry returns the transaction to Pending; • Unique local transaction ID prevents double submission |
| SFA-24 | Camera & Attachment | • Visit photo; • Legal document; • Invoice/transaction evidence; • Payment evidence; • File type and size validation |
| SFA-25 | GPS & Maps | • User and customer location; • Distance calculation; • Visit verification; • Map preview |
| SFA-26 | Barcode / QR Scanner | • Product barcode scan; • IMEI scan; • Manual-entry fallback |
| SFA-27 | Activity History | • Submission and status history; • Approval/rejection; • Rejection reason; • Resubmission; • User and timestamp from CMS |
| SFA-28 | Profile & Settings | • User profile; • Change password; • Notification settings; • Language when required; • Logout |
| SFA-29 | Help & Support | • FAQ; • Privacy policy; • Terms and conditions; • Application version; • Support contact |

## 6. Manager and Approval Features

| ID | Module | Description | Position |
|---|---|---|---|
| SFA-M01 | Mobile Approval Inbox | • Display approvals assigned by CMS; • Partner registration review; • Partner profile-change review; • Warranty Activation / IMEI review; • No second approval for Reward Claim; • Sales Order/discount approval; • Visit reschedule approval; • Open request detail; • Approve/reject/return for revision when permitted; • Mandatory rejection reason; • Approval notification | Confirmed for draft |
| SFA-M02 | Team Monitoring | • Team-performance summary; • Visit monitoring; • Order summary; • Pending approval summary | Review |
| SFA-M03 | Partner Profile Review | • Assigned internal Sales reviews partner-profile changes; • Approve/reject/return for revision; • Current approved profile remains active until approval | Required |
| SFA-M04 | Approval Matrix | • Configured and stored in CMS; • CMS is the authoritative source; • SFA reads assigned approver, level, permitted action, and status; • Do not store authoritative approval configuration in mobile local DB; • Super Admin mobile view can call CMS later if required | Confirmed CMS Boundary |

## 7. Review Decisions

| Decision ID | Topic | Description | Status |
|---|---|---|---|
| DEC-01 | Application Model | • One SFA Mobile application; • Common login and shared mobile foundation; • Different landing page, menu, data, and actions according to role; • Permission and record filtering controlled by CMS | Confirmed: One Role-Based Application |
| DEC-02 | Mobile Approval Scope | • Partner registration review; • Partner profile-change review; • Warranty Activation / IMEI review; • No second manual approval for Reward Claim; • Sales Order/discount approval; • Visit reschedule approval; • No separate collection approval in mobile; • Approval-matrix configuration remains in CMS | Confirmed for draft |
| DEC-03 | Offline Transaction Scope | • User can Confirm selected transactions while offline; • Offline Confirm creates Pending Sync; • Supported: visit, order, Sell-Out/IMEI/warranty, stock receipt, stock Sell-Out, stock opname, collection, and partner quotation draft; • Statuses: Pending, Synced, Failed; • Temporary technical errors stay Pending and auto-retry; • Business validation/permission errors become Failed; • Edit & Resubmit or Retry changes Failed back to Pending; • Final processing and validation remain in CMS | Confirmed direction |
| DEC-04 | Sales Tracking & Visit Conversion | • Dashboard aggregate with list drill-down; • Sell-In and Sell-Out tabs; • Completed Visit with linked order is Converted; • Completed Visit without linked order is Non-Converted; • Multiple orders from one visit count as one Converted Visit; • Visit-to-Order Conversion = Converted Visit / Total Completed Visit x 100% | Confirmed |
| DEC-05 | Outlet Stock | • Single design source: SFA-10 Outlet Stock Movement & Opname; • Receipt creates IN; • Sell-Out creates OUT; • Opname creates Adjustment IN/OUT from the difference between System On Hand and Counted Quantity; • On Hand is authoritative after adjustment; • Partial receipt uses Manual Receipt with a unique derived reference; • Buffer is configured per product in CMS; • Status: Out of Stock, Low Stock, or On Stock; • Opname Due creates an alert and manual Schedule Visit action; • Internal users only see assigned outlets | Provisionally accepted |
| DEC-06 | Collection Submission | • Sales / SPG submits collection data with mandatory attachment; • SFA displays Paid immediately after collection confirmation; • SFA does not display Odoo payment-sync status; • No accounting-journal scope in SFA Mobile; • CMS creates the payment record and manages synchronization to Odoo | Confirmed direction |
| DEC-07 | Reward Mechanism | • Select reward during Warranty Activation / Sell-Out Registration; • Approved warranty activation creates Sell-Out and makes IMEI eligible for Reward Claim; • Dealer/outlet submits Reward Claim as a separate next action; • No separate program selection; • No point balance; • One IMEI can have one approved reward claim; • Approved monetary/dealer-payable claim is prepared by CMS for Vendor Bill integration to Odoo | Confirmed direction; detailed flow deferred |
| DEC-08 | Approval Matrix Location | • Approval matrix is configured and stored in CMS; • SFA Mobile only displays and executes assigned approvals | Confirmed |
| DEC-09 | Discount & Tax | • Price and tax are supplied and validated by CMS; • Unit price and tax are not manually editable in SFA; • Internal Sales can enter line discount within role limit; • Discount above the role limit requires Sales Manager approval; • External Partner cannot enter discount; • Final calculation and rounding are performed by CMS; • Offline transaction uses last-synced terms and is revalidated by CMS; • Global order discount remains open for team discussion | Provisionally accepted - Team review pending |
| DEC-10 | Detailed Reward Flow | • Warranty Activation creates Sell-Out, activates warranty, and makes IMEI eligible; • Reward is selected during Warranty Activation and inherited by Reward Claim; • Reward Claim is submitted as a separate next action; • No additional attachment or second manual review is required; • CMS automatically validates Active warranty and unused IMEI claim; • One IMEI has one Reward Claim and one reward; • Claimed reward is prepared by CMS for Vendor Bill integration | Provisionally accepted - Team review pending |

## 8. Decisions Captured from Review

- Internal and external users can log in after registration and activation.
- Internal and external users use one role-based SFA Mobile application.
- Mobile approval scope includes partner registration/profile, Warranty Activation/IMEI, Sales Order/discount, and visit reschedule.
- Reward Claim uses automated validation and does not require a second manual approval.
- Schedule date/time is replaced only after reschedule approval.
- Sales / Promotor can visit and clock in on the proposed date while reschedule approval is pending.
- Actual check-in/out timestamps always follow the actual transaction timestamp and radius validation.
- Schedule Detail contains a Reschedule History tab/section for all reschedule requests.
- Confirmed collection with mandatory attachment displays the invoice as Paid in SFA.
- Odoo payment-sync status is visible only in CMS.
- Payment synchronization from CMS to Odoo remains a later integration task.
- Partner-profile changes require review by assigned internal Sales.
- Partner-staff registration and activation do not require internal-Sales approval.
- IMEI registration supports scan and manual entry.
- IMEI history is scoped by dealer/customer and access assignment.
- Partner quotation request is merged into the order module with restricted access.
- Separate Quotation Tracking module is removed.
- Reward selection occurs directly during IMEI registration.
- Separate reward-program selection and point balance are removed from current scope.
- Reward summary links registered IMEI and selected reward.
- One IMEI can claim a reward only once.
- Outlet stock uses one lightweight movement ledger and physical-opname process.
- Receipt creates IN and Sell-Out creates OUT.
- Opname creates Adjustment IN/OUT so On Hand equals Counted Quantity.
- Dealer Staff or assigned Sales / SPG can record receipt or perform opname according to access.
- Buffer stock is configured per product in CMS.
- Dashboard displays Out of Stock, Low Stock, On Stock, and Opname Due.
- Partial receipt uses Manual Receipt with a unique derived reference.
- Completing an opname recalculates the next due date.
- Opname Due provides a manual Schedule Visit action instead of automatically creating a visit.
- Outlet stock is accessed from Customer Detail / Visit task instead of a standalone menu.
- Reward Claim is represented in CMS before later Odoo mapping.
- Approval-matrix configuration is confirmed in CMS.
- Discount and tax direction is provisionally accepted and awaits team review.
- Internal user-facing transaction is named Sales Order.
- External user-facing transaction is named Quotation and represents Sell-In.
- Approved Warranty Activation creates Sell-Out and activates the IMEI warranty.
- Reward Claim is submitted separately for an eligible IMEI with Active warranty.
- Approved monetary/dealer-payable Reward Claim is prepared by CMS for Vendor Bill integration to Odoo.
- Offline Confirm creates Pending Sync for supported transactions.
- Synchronization uses Pending, Synced, and Failed statuses.
- Sales Tracking uses dashboard aggregate with Sell-In/Sell-Out list drill-down.
- Visit-to-Order Conversion uses Completed Visits and linked Sales Orders.
- Detailed reward flow is provisionally accepted and awaits team review.

## 9. Source Coverage Check

- Existing internal features covered:
  - Customer Visit.
  - Product Stock.
  - Sales Tracking.
  - Stock Tracking as optional scope.
  - Sales Order.
  - Outstanding Invoice / Billing.
  - Customer and Prospect.
- New target features covered:
  - Dashboard.
  - Quick Order.
  - Notification.
  - Offline status and synchronization.
  - GPS visit verification.
  - Visit-to-order linkage.
- External Phase 2 features covered:
  - Partner registration and login.
  - Partner profile and legal documents.
  - Partner staff.
  - IMEI registration and history.
  - Partner quotation request.
  - Reward catalog, claim, and IMEI-linked summary.
- Architecture boundary preserved:
  - SFA Mobile communicates with CMS.
  - No direct SFA Mobile to Odoo communication.
