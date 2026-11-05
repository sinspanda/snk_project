# MITO SFA Mobile - High-Level Process Draft

**Version:** 0.1  
**Status:** Working Draft - For Internal Review  
**Scope:** SFA Mobile Application  

### Type Classification

- **Standard:** Feature already exists in the current application and can be retained without development changes.
- **Manual:** Activity is performed outside SFA Mobile by a user or through an external operational process, without automated data exchange from SFA Mobile.
- **Customization:** Feature is new or requires development changes within SFA Mobile.
- **Integration:** Activity requires automated data exchange between SFA Mobile and CMS. CMS is shown as the actor when CMS processing or a CMS response is required before the flow can continue.
- When a new SFA feature also requires CMS communication, the SFA activity and CMS integration activity are separated into different activity rows.
- Type classification will be used later as an input for implementation-effort estimation.

### Process Writing Principle

- Activity is written as a business process or business decision, not as a sequence of screen clicks or technical system steps.
- Activity Name uses business-action wording, such as **Confirm Order**, **Review Registration**, **Record Customer Visit**, or **Approve Reschedule**.
- Description explains the business scope, required information, validation, responsibility, and expected outcome.
- Button names, API calls, screen navigation, sync mechanics, and other technical details are documented later in the functional or technical design when required.
- CMS is shown as an actor only when CMS processing or a CMS response represents a meaningful business handoff required to continue the process.

## P01 - User Registration, Activation & Login

### A. Internal User Registration

| Activity ID | Activity Name | PIC | Description | Type |
|---|---|---|---|---|
| P01-INT-01 | Register Internal User | CMS Admin | CMS Admin creates an internal-user account and assigns the appropriate role, customer, outlet, or territory access based on the user's responsibilities. | Manual |
| P01-INT-02 | Validate User Data | CMS | During user registration, CMS checks whether the entered username or email address has already been registered. | Manual |
| P01-INT-03 | Activate Account | CMS Admin | CMS Admin activates the validated internal-user account and prepares the information required by the user to access SFA. | Manual |
| P01-INT-04 | Send Activation | CMS | CMS sends the account-activation notification together with the applicable password creation or reset instruction. | Manual |

### B. External Partner Registration

| Activity ID | Activity Name | PIC | Description | Type |
|---|---|---|---|---|
| P01-EXT-01 | Start Registration | External Partner | The External Partner registers the required personal and business information. | Customization |
| P01-EXT-02 | Complete Registration Documents | External Partner | The External Partner provides the required legal or supporting documents and accepts the applicable terms and conditions. | Customization |
| P01-EXT-03 | Submit Registration | External Partner | The External Partner reviews the completed information and submits the registration request for Internal Sales review. | Customization |
| P01-EXT-04 | Validate Registration | CMS | CMS validates mandatory information and possible duplicate user or business records before recording and assigning the request to the responsible Internal Sales. | Integration |
| P01-EXT-05 | Review Registration | Internal Sales | Internal Sales reviews the partner information and supporting documents, then approves, rejects with a reason, or returns the registration for revision. | Manual |
| P01-EXT-06 | Revise Registration | External Partner | The External Partner reviews the provided reason, corrects the required information or documents, and resubmits the same registration request. | Customization |
| P01-EXT-07 | Activate Partner Account | Internal Sales | Internal Sales activates an approved partner account and assigns its partner organization, role, and permitted data-access scope. | Manual |
| P01-EXT-08 | Provide Approval Result | CMS | CMS provides the latest approval, rejection, or revision status to SFA and makes the account-activation instruction available after approval. | Integration |

### C. Dealer Staff Registration

| Activity ID | Activity Name | PIC | Description | Type |
|---|---|---|---|---|
| P01-STF-01 | Register or Invite Staff | Dealer Owner | The Dealer Owner registers or invites a staff member by providing the required staff information and assigning the appropriate role. Access rights follow the role configuration defined in SFA and CMS. | Customization |
| P01-STF-02 | Validate Staff | CMS | CMS validates the Dealer Owner's authority and possible duplicate user records before linking the staff account to the appropriate dealer organization. | Integration |
| P01-STF-03 | Activate Staff | Dealer Owner | The Dealer Owner activates or deactivates staff access without requiring approval from Internal Sales. | Customization |
| P01-STF-04 | Provide Staff Activation | CMS | CMS provides the staff activation result to SFA and makes the password setup instruction available to the registered staff member. | Integration |

### D. Login

| Activity ID | Activity Name | PIC | Description | Type |
|---|---|---|---|---|
| P01-LOG-01 | Enter Credentials | User | The user enters the registered identifier and password to access the SFA application. | Standard |
| P01-LOG-02 | Authenticate User | CMS | CMS authenticates the submitted credentials and confirms that the account, role, and related organization are active and permitted to use SFA. | Integration |
| P01-LOG-03 | Load User Access | CMS | CMS provides SFA with the user's role, permitted menus, and assigned customer, dealer, outlet, or territory access. | Integration |
| P01-LOG-04 | Initialize Mobile Access | SFA Mobile | SFA establishes access based on the authorized scope, prepares the permitted offline data, and displays the dashboard corresponding to the user's role. | Customization |
| P01-LOG-05 | Access SFA Offline | User | The user may continue accessing SFA through an existing valid local session, while the first login and authentication of a new or expired session must be completed online. | Customization |
| P01-LOG-06 | Change Password | User | The user requests a password change by confirming the current password and providing a new password that complies with the applicable password policy. | Standard |
| P01-LOG-07 | Update User Password | CMS | CMS validates the password-change request and updates the user's login credential for subsequent SFA access. | Integration |
| P01-LOG-08 | Log Out from SFA | User | The user ends the active SFA session so that the application can no longer be accessed through the signed-in account without logging in again. | Standard |

### E. Account Status

- Draft.
- Pending Approval.
- Revision Required.
- Approved.
- Active.
- Rejected.
- Inactive.
- Blocked.

### F. Process Output

- User account is active.
- User role is assigned.
- Data-access scope is assigned.
- User can log in to the role-based SFA Mobile application.
- Dashboard and menu follow the assigned role.

## P02 - Dashboard & Work Overview

### A. Dashboard Information

| Activity ID | Activity Name | PIC | Description | Type |
|---|---|---|---|---|
| P02-DSH-01 | Provide Dashboard Information | CMS | CMS provides the latest visit, order, revenue, outlet-stock, and work-activity information according to the user's role and assigned data scope. | Integration |
| P02-DSH-02 | Review Sales Activity Summary | Sales / Sales Manager | Sales and Sales Manager review actual visits, orders, and available revenue information to understand current sales activity and performance. | Customization |
| P02-DSH-03 | Review Visit Conversion | Sales / Sales Manager | Sales and Sales Manager review completed visits with orders, completed visits without orders, and the resulting Visit-to-Order Conversion for the selected period. | Customization |

### B. Work Priority & Follow-Up

| Activity ID | Activity Name | PIC | Description | Type |
|---|---|---|---|---|
| P02-WRK-01 | Review Daily Work Priority | Sales | Sales reviews today's activities and pending work to determine the customer visits and follow-up actions that require attention. | Customization |
| P02-WRK-02 | Review Outlet Stock Priority | Sales / Sales Manager | Sales and Sales Manager review assigned outlets categorized as Out of Stock, Low Stock, On Stock, or Stock Opname Due to determine the required commercial follow-up. | Customization |
| P02-WRK-03 | Follow Up Dashboard Information | Sales | Sales opens the relevant customer, outlet, visit, order, or activity information from the dashboard and continues with the appropriate business process. | Customization |
| P02-WRK-04 | Schedule Visit from Stock Priority | Sales | Sales schedules a customer or outlet visit when a stock condition or Stock Opname Due requires direct follow-up. The dashboard does not create the visit automatically. | Customization |

### C. Team Overview

| Activity ID | Activity Name | PIC | Description | Type |
|---|---|---|---|---|
| P02-MGR-01 | Review Team Performance | Sales Manager | Sales Manager reviews summarized visit, order, revenue, and Visit-to-Order Conversion information for Sales users within the manager's authorized team scope. | Customization |
| P02-MGR-02 | Review Team Workload | Sales Manager | Sales Manager reviews team activities and pending work to identify users, customers, or outlets that require attention or follow-up. | Customization |

### D. Integration Staging

| Activity ID | Activity Name | PIC | Description | Type |
|---|---|---|---|---|
| P02-INT-01 | Review Integration Staging | Super Admin | Super Admin reviews SFA transactions exchanged with CMS, including Pending, Synced, and Failed records, to monitor and follow up the integration process. | Integration |

### E. Scope Notes

- Dashboard information is limited by the user's role, customer/outlet assignment, territory, and team access.
- CMS is the source of dashboard business information provided to SFA Mobile.
- Customer-level annual or monthly revenue targets are excluded from the minimum scope.
- Stock-priority information provides a Schedule Visit action but does not automatically create a visit.
- Integration Staging on the dashboard is available only to Super Admin.
- Dashboard implementation is categorized as a lower-priority scope for the current draft.

## P03 - Customer Registration

### A. Prospect Management & Customer Confirmation

| Activity ID | Activity Name | PIC | Description | Type |
|---|---|---|---|---|
| P03-PRO-01 | Register Prospect | Sales / Promotor / GTM | Sales, Promotor, or GTM registers the Prospect information, responsible Salesperson, and applicable business segment such as Retail or Pareto. | Customization |
| P03-PRO-02 | Record Prospect | CMS | CMS validates the required information and possible duplicate data before storing the Prospect in CMS. The Prospect is not sent to Odoo. | Integration |
| P03-PRO-03 | Manage Prospect | Sales / Promotor / GTM | Sales, Promotor, or GTM performs the required approach and commercial follow-up with the Prospect until a deal decision is reached. | Manual |
| P03-PRO-04 | Confirm Prospect as Customer | Assigned Salesperson | When a deal is reached, the assigned Salesperson confirms the Prospect as a Customer through SFA. | Customization |
| P03-PRO-05 | Update Prospect to Customer | CMS | CMS updates the existing record's status or type from Prospect to Customer, retains the same Salesperson and segmentation, and sends the Customer data to Odoo. | Integration |

### B. Scope Notes

- Prospect data is stored in CMS and is not sent to Odoo.
- Prospect segmentation uses business categories such as Retail, Pareto, and other segments maintained in CMS.
- The responsible Salesperson can be a Sales, Promotor, or GTM user according to the assignment.
- Prospect management and commercial follow-up are performed manually by Sales, Promotor, or GTM.
- Prospect remains a Prospect until the assigned Salesperson confirms the deal through SFA.
- CMS updates the same record from Prospect to Customer without creating duplicate master data.
- Only records with Customer status/type are integrated from CMS to Odoo.
