# Race Manager Pro — TODO

## Backlog
- [ ] Widget addition UI (add widgets—including DocViewerWidget—to views/containers via "+" button)
- [ ] View layout save/load (serialize/deserialize views)
- [ ] Saved views menu (list, load, rename, delete views)
- [ ] Drag-and-drop widget arrangement
- [ ] User doc viewer: index, search, and navigation
- [ ] Telemetry/Timing/Other widgets
- [ ] Real-time data integration
- [ ] In-app help/manual
- [ ] User onboarding flow
- [ ] Document best practices for dynamic widget/container management in dev docs (always use a root container, avoid direct layout manipulation in views)
- [ ] Add HTML rendering for support documents (QWebEngineView) when stable on Linux. Currently using plain markdown in QTextEdit due to segfaults.

## In Progress
- [ ] Make BlankView truly empty and ready for widget addition
- [ ] Implement widget/panel addition UI (including DocViewerWidget) in BlankView

## Done
- [x] DocViewerWidget implemented
- [x] requirements.txt restored from venv
- [x] Session summary and lap chart widgets (table and graph)
- [x] Centralized edit mode propagation
- [x] Modular, extensible UI structure

## Bugs
- [x] "Add Widget" only adds DocViewerWidget; should allow choosing any available widget type. (Fixed)
- [x] DocViewerWidget only displays plain text, not formatted markdown (should support rich markdown rendering in QTextEdit or similar). (Fixed)
- "Add Panel" always creates vertical panels, regardless of selection; horizontal orientation is ignored.
- There are more resize handles than expected; investigate QSplitter usage and layout structure.
- [x] Edit mode controls (split/add buttons) do not appear when toggling edit mode. Investigate propagation and widget visibility issues. (Fixed: set_edit_mode now propagates from BlankView to root LayoutContainer)

---

*Add new ideas, bugs, or improvements below as you work!*

- [ ] Refactor BlankView to use QSplitter for dynamic widget management (robust with QWebEngineView)
- [ ] Document QSplitter-based dynamic UI pattern in developer docs
