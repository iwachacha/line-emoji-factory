# Project Map

This repository is a startup project for `[BRAND_NAME]`.

## Purpose

The repo isolates brand-specific context after the factory has enough structure to keep the concept. It is not a full production or submission repo by default.

## Directories

- `brand/`: brand setting, canon, positioning, production brief seed, system prompt, and product catalog seed.
- `startup/`: startup brief and startup checklist.
- `data/`: character / motif data, item seed data, and asset log template.
- `prompts/`: reusable prompt library.
- `market/`: observation notes and gap hypotheses.
- `references/shared/`: snapshot of required factory rules and workflows.
- `schemas/`: validation schemas.
- `tools/`: lightweight validation tools.

## Standard Flow

1. Confirm structure in `startup/brand-startup.md`.
2. Fix the minimum brand core in `brand/brand-setting.md`.
3. Set guardrails in `brand/brand-canon.md`.
4. Seed product hypotheses in `data/item-seeds.json`.
5. Prepare prompts in `prompts/prompt-library.md`.
6. Validate with `python tools/validate-brand-repo.py .`.

## Promotion Trigger

Add production release directories only when the brand has a clear first set, rough anchor needs, or real asset production.
Run `tools/promote-brand-repo.ps1` from the factory repo, or pass `-FactoryRoot` when using the copied tool inside this brand repo.
