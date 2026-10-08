# Inspection Tracker

A PySide6 desktop app with the existing inspection dashboard, summary counts,
inspection cards, sortable table, and add/edit/complete/delete dialogs. Clicking
cards opens editable details; clicking table rows opens read-only details.
SQLAlchemy models and scheduling rules remain unchanged. No web server is needed.

## Run from source

Use Python 3.13 or newer:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

## Build a single Windows EXE

On Windows, install Python 3.13 on the build machine and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\build_windows.ps1
```

Distribute `dist\InspectionTracker.exe`. End users do not need Python, Qt, or
other dependencies installed. PyInstaller embeds them and extracts runtime files
to a temporary directory on launch, so first startup can take a few seconds.
Build Windows executables on Windows; Linux builds cannot produce a Windows EXE.

Alternatively, commit these files to GitHub and manually run **Build Windows
executable** in Actions. Download the InspectionTracker-Windows artifact and
extract the EXE. The workflow runs tests before packaging. Before distribution,
test the EXE on a Windows computer without Python installed.

References: [PyInstaller packaging](https://pyinstaller.org/en/stable/operating-mode.html)
and [Qt deployment](https://doc.qt.io/qtforpython-6/deployment/deployment-pyinstaller.html).

## Database and existing data

Data is stored separately from the executable, so app updates do not overwrite it:

- Windows: `%LOCALAPPDATA%\InspectionTracker\inspections.db`
- Linux/macOS: `$XDG_DATA_HOME/InspectionTracker/inspections.db`, defaulting to
  `~/.local/share/InspectionTracker/inspections.db`.

To migrate existing data, close the old app and any database tools first. Back up
its `inspections.db`, then copy it into the location above before launching the
new app. No schema conversion is required. If WAL sidecar files exist, use SQLite's
backup facility rather than copying an active database file.

For a custom database location, set `INSPECTION_TRACKER_DB` to the full database
path before starting the app. This also isolates development and test databases.
The app uses WAL and a five-second lock timeout; database failures show a dialog
and are logged to `inspection-tracker.log` beside the database. WAL reduces
reader/writer contention but does not allow simultaneous writers. Keep the database
on a local disk. Writes run on the GUI thread and may pause the UI while waiting
for a lock (up to five seconds).

`test_data.py` is a destructive sample-data script: it drops the inspection table.
Only run it with `INSPECTION_TRACKER_DB` pointing to a disposable database.

## Tests

```sh
QT_QPA_PLATFORM=offscreen python -m unittest discover -s tests -v
```

On PowerShell set `$env:QT_QPA_PLATFORM = "offscreen"` first, then run the Python
command. Tests use a temporary database and never touch user data.
