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

---

*This document is a living reference for the software design of Race Manager Pro. Update as the project evolves.*
