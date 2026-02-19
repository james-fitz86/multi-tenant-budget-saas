# Architecture Overview

## Purpose

This project models a multi-tenant SaaS platform for departmental budget governance and structured spend approval workflows.

The focus of this system is architectural maturity — modelling organisational scoping, financial controls, and conditional workflow logic within a clean, scalable backend structure.

---

## Multi-Tenancy Strategy

This system uses **row-level multi-tenancy**.

Each Organisation acts as a tenant.
All tenant-bound models include a foreign key to Organisation to ensure strict data isolation.

Data access will always be scoped to the user’s organisation membership.

---

## User & Role Model

Users may belong to one or more Organisations.

Roles are assigned at the Organisation level via an OrganisationMembership model.

This allows a user to have different roles in different organisations.

Example roles:
- Employee
- Department Manager
- Finance
- Organisation Admin

Permissions are enforced based on organisation membership and assigned role.

---

## Core Domain Entities

Initial core entities include:

- User (custom)
- Organisation
- OrganisationMembership
- Department
- Budget
- SpendCategory
- SpendRequest
- Approval
- AuditLog

Additional entities may evolve as business rules develop.

---

## Architectural Principles

- Explicit organisational data scoping
- Clear separation of concerns between apps
- Business-rule driven workflow modelling
- Auditability of financial actions
- Role-based access enforcement at the organisational level
- Designed for future containerisation and production deployment

---

## Status

Initial architecture definition phase.
Models and tenancy boundaries are currently being designed.
