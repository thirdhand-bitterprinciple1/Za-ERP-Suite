# Use Cases

This document lists practical business scenarios supported by ZA ERP Suite.

## 1) Multi-company Operations

- A single user can belong to multiple companies.
- API requests are isolated by `X-Company-ID`.
- Data leakage across companies is prevented by company-scoped models/querysets.

## 2) Sales to Accounting Automation

- Sales user creates a sales order.
- Order moves from Draft to Pending Approval.
- Manager/Admin approves the order.
- System posts accounting entries and updates inventory automatically.

## 3) Purchasing and Stock Replenishment

- Purchasing user creates supplier and purchase order.
- PO is submitted for approval.
- Manager/Admin approves.
- Stock is increased automatically via domain events.

## 4) Audit and Accountability

- Create/update/delete operations generate audit records.
- Logs include actor, timestamp, and before/after values.
- Admin/Manager can review logs via API.

## 5) Real-time Notification Workflow

- Report completion/failure creates notifications.
- Notifications stream over SSE.
- User can mark one or all notifications as read.
- Notification deep-linking can route user to related module records.

## 6) Monthly Reporting

- Accounting user requests monthly P&L report job.
- Celery processes report in background.
- PDF file is generated and linked to report job.
- User can download completed report file.

## 7) Role-based Permissions

- Sales, Inventory, Purchasing, Accounting, HR, Projects, Manager, Admin roles.
- Approval endpoints restricted to Manager/Admin.
- Module APIs enforce role boundaries.
