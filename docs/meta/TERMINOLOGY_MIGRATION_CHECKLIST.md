# Race Manager Pro — Terminology Migration Checklist

## Purpose
This checklist tracks the migration from old UI terms to the new, more intuitive terminology:
- **Dashboard** (was: View)
- **Divider** (was: Container, LayoutContainer)
- **Panel** (was: Widget)

---

## Migration Steps

### 1. Codebase Refactor
- [ ] Rename all class names, filenames, and variables:
    - `*View` → `*Dashboard`
    - `LayoutContainer` → `Divider`
    - `*Widget` → `*Panel`
- [ ] Update all import statements and references.
- [ ] Update UI text (button labels, tooltips, menus) to use new terms.
- [ ] Update comments and docstrings throughout the codebase.

### 2. Documentation
- [ ] Update all documentation files:
    - `SOFTWARE_DESIGN.md`
    - `TODO.md`
    - `UI_USER_STORIES.md`
    - Any user or developer docs referencing old terms
- [ ] Update diagrams or screenshots if present.

### 3. Communication & Onboarding
- [ ] Announce terminology change to all contributors.
- [ ] Update onboarding/readme materials to explain new terms.

### 4. Testing
- [ ] Test the UI to ensure all references and controls use the new terms.
- [ ] Confirm that no old terminology remains in user-facing text or code.

---

*Check off each item as you complete it. Update this checklist as needed during the migration process.*
