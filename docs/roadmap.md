# Development Roadmap

This roadmap outlines the phased architectural evolution of the platform.  
Each phase represents a structural milestone in developing a multi-tenant SaaS system focused on financial governance and organisational control.  
Phases may evolve as domain understanding deepens and implementation insights emerge.

---

## Phase 1 — Core Identity & Tenant Foundation

- Establish platform-level identity with a custom User model.
- Introduce Organisation as the core tenant entity with self-service creation.
- Implement OrganisationMembership to support multi-organisation access and role assignment.
- Define enum-based organisational roles with centralised permission mapping.
- Enforce row-level multi-tenancy with scoped data access patterns.
- Introduce a service-layer pattern to centralise domain logic and maintain thin API views.

---

## Phase 2 — Organisational Structure & Budget Domain

- Introduce a time-bound OrganisationBudget model supporting monthly, quarterly, and yearly periods.
- Implement Department entities scoped strictly to a single Organisation.
- Model DepartmentBudget allocations derived from the OrganisationBudget with enforced allocation limits.
- Enforce hard financial constraints preventing over-allocation beyond the organisation’s total budget.
- Implement committed vs actual spend tracking to provide accurate real-time budget visibility.
- Introduce recurring commitments to automatically reserve fixed expenses within each budget period.

---

## Phase 3 — Spend Requests & Governance Workflow

- Introduce structured SpendRequest submission scoped to department budgets.
- Implement approval workflows based on organisational roles and spend thresholds.
- Model workflow state transitions with service-layer enforcement.
- Prevent over-commitment by validating against available budget at approval time.
- Record governance actions within an auditable activity trail.

---

## Phase 4 — Audit, Oversight & Reporting Foundations

- Implement an AuditLog system to track key financial and governance actions.
- Introduce budget visibility dashboards for organisational and departmental views.
- Provide burn-rate and period-based reporting insights.
- Establish foundational notification triggers for governance events.
- Strengthen data integrity safeguards and historical record preservation.

---

## Phase 5 — API Layer & Access Control Hardening

- Introduce a formal API layer to expose domain functionality.
- Implement structured authentication and role-based access enforcement.
- Standardise permission checks across service-layer operations.
- Enforce consistent tenant scoping at the API boundary.
- Prepare backend for decoupled frontend integration.

---

## Phase 6 — Frontend Integration & Client Decoupling

- Introduce a React-based SPA consuming backend APIs.
- Implement organisation-aware routing and context switching.
- Develop dashboards for budget visibility and governance workflows.
- Provide structured UI flows for spend submission and approvals.
- Align frontend state management with tenant-scoped API design.

---

## Phase 7 — Infrastructure, Containerisation & Deployment

- Containerise backend, frontend, and database services.
- Introduce environment-based configuration management.
- Implement reverse proxy and production-ready deployment structure.
- Harden security configuration for multi-tenant operation.
- Prepare system for scalable SaaS-style hosting.
