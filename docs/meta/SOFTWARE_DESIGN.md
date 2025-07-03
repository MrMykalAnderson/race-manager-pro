# Race Manager Pro — Software Design Document

## 1. Introduction
This document describes the architecture, design principles, and major components of Race Manager Pro. It is guided by the project's goals and features as outlined in the Goals and Features document.

## 2. Vision & Scope
Race Manager Pro is a desktop application for motorsport data browsing and simulation, targeting both gamers and motorsport professionals. It aims to provide highly customizable, real-time data views and deep simulation features.

## 3. Architecture Overview
- **Platform:** Desktop (Windows, Mac, Linux)
- **Framework:** PySide6 (Qt for Python)
- **Structure:** Modular, component-based UI with extensible widgets and views
- **Data Flow:** Real-time updates, with future support for external data feeds

## 4. Major Components
### 4.1 UI Layer
- **Main Window:** Manages tabs and global actions
- **Views:** Customizable dashboards (e.g., BlankView, DefaultView)
- **Widgets:** Modular, reusable UI elements (e.g., TestWidget, LayoutContainer, SessionSummaryWidget, LapChartWidget)
- **Edit Mode:** Centrally managed via Qt signals; all widgets and containers update automatically

### 4.2 Simulation Engine (Planned)
- **Race Model:** Data structures for races, teams, drivers, and events
- **Simulation Logic:** Engine for running race and championship simulations (**basic version implemented**)
- **Real-Time Updates:** Mechanism for updating UI as simulation progresses (UI ready, integration pending)

### 4.3 Data Integration (Future)
- **Live Data Feeds:** Interfaces for real/sim racing data sources
- **Data Adapters:** Convert external data to internal models

### 4.4 Documentation & Help
- **Markdown Docs:** User manual and help files accessible in-app
- **API Docs:** Generated from code docstrings

## 5. Key Design Principles
- **Customizability:** Users can arrange and configure views and widgets
- **Extensibility:** Easy to add new widgets, views, and data sources (widget library is easily extensible)
- **Responsiveness:** UI updates in real time as data changes
- **Maintainability:** Modular code, clear separation of concerns, thorough documentation
- **Qt signals are used for state propagation (edit mode)**

## 6. User Experience Flow
1. User launches app and selects or creates a dashboard view
2. User customizes layout and widgets as desired
3. Before a race, user prepares views to monitor key data
4. During a race, user interacts with real-time data and simulation controls
5. User can access help/manual at any time
6. Users can switch views and see live-updating widgets

## 7. Data Storage Strategy
- **Session Results:** Each simulated or real race session (including lap times, telemetry, and events) is stored as a separate JSON file in a dedicated `data/sessions/` directory.
- **User Data:** User preferences, custom views, and user-created sessions or championships are stored in `data/users/` as JSON files.
- **History:** All past sessions are accessible for review, comparison, and analysis.
- **Portability:** All data can be imported/exported as JSON for sharing or backup.
- **Performance:** For large telemetry datasets, consider splitting telemetry into separate files or using a lightweight database (e.g., SQLite) in the future.
- **Directory Structure Example:**
  ```
  race-manager-pro-1/
    data/
      sessions/
        2025-07-02_4car_oval.json
        ...
      users/
        user1.json
        ...
    docs/
    sim/
    ...
  ```

## 8. Future Considerations
- 3D visualization of races
- Advanced analytics and strategy tools
- Cloud sync and multi-user collaboration

## 9. Developer Notes: Views, Widgets, and Best Practices

### How the UI Code Works
- **Views** (e.g., `BlankView`, `DefaultView`) are top-level containers for user dashboards. Each view is a `QWidget` subclass and is added as a tab in the main window.
- **Widgets** are modular UI elements (e.g., summary tables, charts, containers) that are added to views or to layout containers within views.
- **Layout Containers** (e.g., `LayoutContainer`) are special widgets that manage the arrangement of child widgets using Qt layouts or splitters. All dynamic content in a view should be managed through a root container widget.
- **Edit Mode** is propagated via Qt signals, allowing all widgets and containers to update their UI state (e.g., show/hide controls) in sync.

### Best Practices & Lessons Learned (from segfault debugging)
- Always use Qt enums (e.g., `Qt.AlignHCenter`) for alignment, not raw integers.
- Add widgets and layouts incrementally, testing after each change to quickly isolate issues.
- Avoid custom styling, fixed sizes, or alignment until basic widget logic is confirmed stable.
- Let Qt handle layout and appearance by default; only add custom styles after confirming stability.
- When subclassing Qt widgets, always call `super().__init__()` first.
- If a segfault occurs on basic widget creation, revert to the simplest working version and reintroduce features step by step.
- Use logging at each step of widget/view construction for easier debugging.
- Avoid direct manipulation of layouts in views; always use a root container widget for dynamic content.

## 10. Recent Architectural Updates & Lessons Learned (2025-07)

### 10.1 Recursive LayoutContainer System
- The UI now uses a recursive, splitter-based `LayoutContainer` system for all dynamic/nested layouts.
- Every view (e.g., `BlankView`) must have a single root `LayoutContainer` that manages all child widgets and containers.
- Users can add vertical/horizontal splitters and widgets at any container location, supporting highly flexible layouts.

### 10.2 Widget Registry Pattern
- All available widgets are registered in a central registry (`ui/widgets/registry.py`).
- The "Add Widget" menu dynamically lists all registered widgets, making the UI extensible without code changes in the core UI.

### 10.3 Edit Mode Controls & Propagation
- Edit mode overlay controls (split/add buttons) are implemented as a floating widget in each `LayoutContainer`.
- Edit mode is toggled globally via Qt signals and must be propagated from the view (e.g., `BlankView`) to the root container and all descendants.
- Always implement a `set_edit_mode` method in views and containers to ensure correct propagation.
- After toggling edit mode, force a UI update/repaint if controls do not appear as expected.

### 10.4 Debugging & Logging
- File logging (`race_manager.log`) is enabled for post-mortem debugging and tracking UI state changes. The log file is created in the project root and overwritten on each run.
- By default, logging is set to `INFO` level for all modules to reduce noise and focus on important UI actions, state changes, and errors. Use `DEBUG` only for deep troubleshooting.
- Noisy third-party loggers (e.g., `matplotlib`, `qt`, `PySide6`) are set to `WARNING` to keep the log file concise and relevant.
- You can adjust logging levels for your own modules (e.g., `main`, `LayoutContainer`) in `main.py` for more or less verbosity as needed.
- Only high-level UI actions (splits, widget adds, deletes, mode toggles), errors, and key state changes are logged by default.
- Avoid logging excessive geometry, font, or Qt internals unless actively debugging those areas.
- Add granular debug logging for widget/control creation, edit mode changes, and layout operations only when needed for troubleshooting.
- Review and prune logging statements regularly to keep logs actionable and maintainable.

### 10.5 Best Practices (2025-07)
- Always use a root `LayoutContainer` for all dynamic content in a view; never manipulate layouts directly in views.
- Use Qt enums for alignment and avoid raw integers.
- Add widgets/layouts incrementally and test after each change.
- Let Qt handle layout and appearance by default; only add custom styles after confirming stability.
- When subclassing Qt widgets, always call `super().__init__()` first.
- If a segfault occurs, revert to the simplest working version and reintroduce features step by step.
- Use logging at each step of widget/view construction for easier debugging.
- Propagate edit mode from the view to the root container and all children.
- After UI state changes, call `update()` or `repaint()` if needed to ensure visibility.

### 10.6 Known Issues & Future Improvements
- "Add Panel" always creates vertical panels, regardless of selection; horizontal orientation is ignored.
- There are more resize handles than expected; review QSplitter usage and layout structure.
- Consider adding more granular debug logging to `LayoutContainer` for widget/control creation and edit mode changes.
- Refactor and document best practices for dynamic layouts and widget management as the codebase evolves.

---

*This document is a living reference for the software design of Race Manager Pro. Update as the project evolves.*
