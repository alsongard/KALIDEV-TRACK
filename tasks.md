### Prioritization Plan for KALIDEV-TRACK

Based on your list, I recommend tackling the features in an order that **builds the core functionality first**, then adds enhancements. Here’s a suggested roadmap with reasoning:

---

#### ✅ 1. **View Projects** – **Start Here**
- **Why first?**  
  - It’s the entry point to see what projects exist.  
  - It validates that your file‑system structure works and that you can read project data.  
  - It gives immediate visual feedback and a foundation to test other features.

- **What to implement:**  
  - List all project directories under `PROJECTS/`.  
  - Display them in a `QListWidget` or `QTableView` (with project name, maybe last modified).  
  - Handle empty state (no projects yet).

---

#### ✅ 2. **Add Task for Project** (Create new project)
- **Why second?**  
  - Once you can view projects, you need to add new ones.  
  - This will create the directory structure and the initial `projectdata.json` / `projecttasks.json` files.  
  - It sets up the data for the next features (Edit, Detail).

- **What to implement:**  
  - A dialog to enter project name and initial fields.  
  - Create the directory and write the JSON files.  
  - Refresh the view after adding.

---

#### ✅ 3. **Click on Project to Open Details** (View project details + tasks)
- **Why now?**  
  - After adding a project, you want to see its details.  
  - This brings you to the **task management view** (which you already have some code for).  
  - It leverages the existing `TaskManagement` view.

- **What to implement:**  
  - Connect the table/list click signal to open the project page.  
  - Pass the project name to load its tasks.

---

#### ✅ 4. **Edit Projects** (Modify existing project data)
- **Why fourth?**  
  - Now that you have projects and can view them, editing is a natural next step.  
  - Reuses the same dialog/form as “Add” but pre‑fills with existing data.  
  - Updates the JSON file.

- **What to implement:**  
  - Open a dialog with project fields filled.  
  - Save changes back to `projectdata.json`.

---

#### ✅ 5. **Sync (Backup to MongoDB)**
- **Why later?**  
  - It’s an extra feature, not required for the core usage.  
  - Depends on having a stable data structure to backup.

- **What to implement:**  
  - Add a settings dialog to enter Mongo URI.  
  - Button to trigger backup of all projects.

---

#### ✅ 6. **Settings**
- **Why later?**  
  - Can be added after core features are stable.  
  - Focus on the most used functions first.

- **What to implement:**  
  - Create a `settings.json` file to store app preferences (theme, paths, etc.).  
  - Provide a dialog to edit them.

---

#### ✅ 7. **UI Polishing & Styling**
- **Do throughout, but final polish at the end.**  
  - Start with a minimal, functional UI.  
  - Once all features work, invest time in making buttons look active when checked, consistent fonts, etc.  
  - This reduces the risk of style changes breaking layout early.

---

#### ✅ 8. **ExitApp** (Already works – keep it)

---

### Summary Table

| Order | Feature | Dependencies |
|-------|---------|--------------|
| 1 | View Projects | File‑system reading |
| 2 | Add Task / Project | View Projects (to see result) |
| 3 | Open Details (click project) | View Projects, Add Task |
| 4 | Edit Projects | Add Task (same form) |
| 5 | Sync | Stable data |
| 6 | Settings | None (standalone) |
| 7 | UI Styling | After core is stable |

---

### Next Step

Start with **View Projects**. Implement a simple `QListWidget` that scans `PROJECTS/` and displays each project name. Then, once that works, move to **Add Task** by creating a new project directory and writing initial JSON. This gives you a working loop: create → view → open details → edit.

This approach minimizes frustration and gives you a working application early. You can test each step independently.







# KALIDEV-TRACK — Task Management Module Task List

| Task | Description | Status |
| --- | --- | --- |
| **Fix QGroupBox bug in subtask view** | Previously discovered when testing with mock data: QGroupBox for subtasks is not rendering correctly. Investigate `setWidgetResizable(True)` on scroll area, widget parent/layout nesting, and whether the group box is being added before or after the layout is attached. | ⏳ Pending |
| **Test TaskView in isolation with mock data** | Create a standalone runner (e.g., `if __name__ == "__main__"` in the tasks_view file) that loads a fixed JSON payload and displays the view. Verify: phase name, phase goal, subtask table (Module/Description/Status columns), and any action buttons render correctly. | ⏳ Pending |
| **Test EditTaskView / AddSubtaskDialog in isolation** | Repeat the standalone testing pattern for the add/edit views. Confirm form fields populate from existing data, validate that entered values are captured, and confirm the "cancel" path leaves no side effects. | ⏳ Pending |
| **Define the task JSON schema** | Lock down the exact structure of `project_tasks.json` (fields: `phases → name, goal, subtasks → subtaskname, description, status`). Document it in `docs/data_format.md` so all views and file operations agree on the shape. | ⏳ Pending |
| **Add `read_project_tasks(project_name)` to FileManager** | New method that takes a project name, locates `PROJECTS/<name>/project_tasks.json`, and returns the parsed list. Handle the "file does not exist" case by returning an empty list. | ⏳ Pending |
| **Decide on write strategy for tasks** | Compare: (A) rewrite the whole `project_tasks.json` from the in-memory list each time vs (B) surgical partial updates. **Recommendation:** go with (A) — simpler, atomic, and safe as long as the whole list is held in memory while editing. Document the reasoning in the method docstring. | ⏳ Pending |
| **Add `write_project_tasks(project_name, tasks_data)` to FileManager** | Serializes the full in-memory task list back to `project_tasks.json`. Use `json.dump(..., indent=4)`. Wrap in try/except for `OSError` and `PermissionError`. Log success/failure via `logger`. | ⏳ Pending |
| **Add `add_subtask(project_name, phase_index, subtask_dict)` to FileManager** | Convenience helper: reads tasks, appends to the correct phase's subtasks list, then calls `write_project_tasks`. Keeps view code free of read-modify-write logic. | ⏳ Pending |
| **Add `update_subtask(project_name, phase_index, subtask_index, updated_dict)` to FileManager** | Same pattern as above but replaces an existing subtask. Returns the updated list so the view can refresh its model without a second disk read. | ⏳ Pending |
| **Add `delete_subtask(project_name, phase_index, subtask_index)` to FileManager** | Removes the subtask and writes the file back. Used by the task row's "delete" action (when implemented). | ⏳ Pending |
| **Wire the subtask TableModel into the phase QGroupBox** | Ensure each phase's `QTableView` uses a `TableModel` fed by `phase["subtasks"]` rather than a flat list. Confirm `rowCount()`, `columnCount()`, and `data()` reflect the subtask dict keys (`subtaskname`, `description`, `status`). | ⏳ Pending |
| **Handle the "empty phase" case in the view** | If a phase has zero subtasks, show a placeholder label ("No subtasks yet") instead of an empty table. Prevents a confusing blank group box. | ⏳ Pending |
| **Refresh the view after any write operation** | After `add/update/delete_subtask`, call `load_project_tasks()` or reset the model so the UI reflects the change immediately. Use `beginResetModel`/`endResetModel` on the subtask model, or rebuild the phase group boxes. | ⏳ Pending |
| **Wire the TaskView close signal to the parent (HomeView)** | Mirror the pattern used in `EditSingleProjectView`: `closed = Signal()` in TaskView, emit from `closeEvent`, connect in HomeView to clear the reference (`self.task_view = None`). | ⏳ Pending |
| **Integrate TaskView launch into HomeView** | In HomeView, when a project row's action is triggered (double‑click, "Manage Tasks" button, or context menu), open TaskView with the selected `project_name`. Use the same "one instance at a time" pattern already used for `EditSingleProjectView`. | ⏳ Pending |
| **Pass `user_id` and `project_name` into TaskView** | TaskView needs both to locate the correct JSON file and to stamp new subtasks with the owning user. Extend the constructor: `TaskView(project_name, user_id)`. | ⏳ Pending |
| **Add "Add Subtask" button per phase** | Each phase group box should have an "Add Subtask" button. Clicking it opens a small dialog (or inline form) with fields: `subtaskname`, `description`, `status`. On save → `add_subtask` → refresh. | ⏳ Pending |
| **Add "Edit" action per subtask row** | Use `QStyledItemDelegate` (as done in the projects view) to render an "Edit" button per row, or a context menu on right‑click. Opens the same dialog pre‑filled with existing values → `update_subtask`. | ⏳ Pending |
| **Add "Delete" action per subtask row** | Same pattern as Edit. Confirm with a `QMessageBox` before deleting. Calls `delete_subtask` and refreshes. | ⏳ Pending |
| **Style status column with icons/colors** | In the subtask `TableModel.data()`, handle `Qt.DecorationRole` or `Qt.ForegroundRole` to show ⏳ Pending / ✅ Completed / 🚧 In Progress with matching colors. Makes the table scannable at a glance. | ⏳ Pending |
| **Write unit tests for FileManager task methods** | `pytest` tests using `tmp_path` to verify: read returns empty list for missing file, add appends correctly, update replaces only the target subtask, delete removes only the target. | ⏳ Pending |
| **Add logging throughout the module** | Replace remaining `print()` calls with `logger.debug/info/warning/error`. Log each FileManager operation with the project name and affected indexes. | ⏳ Pending |
| **Document TaskView in `docs/architecture.md`** | Add TaskView to the Mermaid diagram showing HomeView → TaskView → TableModel → FileManager relationships. Keep the architecture doc current as new views land. | ⏳ Pending |



---

## Suggested Execution Order

1. **Fix the QGroupBox bug** — unblocks visual testing of everything else.
2. **Define the JSON schema** — write it down before writing code that assumes a shape.
3. **Add FileManager task methods** — read, write, add, update, delete. Test them with `pytest` before touching any UI.
4. **Wire the subtask TableModel into the phase group box** — get the read‑only display working first with mock data.
5. **Standalone‑test TaskView** — with mock data, confirm phases, goals, tables, and empty states all render.
6. **Add action buttons** (Add / Edit / Delete subtask) — one at a time, refreshing the view after each.
7. **Integrate into HomeView** — reuse the child‑window + `closed` signal pattern.
8. **Polish** — icons, colors, logging, docs.



- File Initation for project_task.json is the below:
```json
{
	"project": "project-name", 
	"phases": []
}
```

The structure for the project_task.json is: 

```json
{
	"project": "project_name", 
	"phases": [ // phases is an array of dictionary with the following structure
		{
			"name": "some name of the phase",
			"goal": "some goal for the phase", 
			"subtasks": [
				{
					"subtaskname": "subtask name",
					"description": "description of subtasks",
					"status": "Pending/Completed",
					"status_note": "some status note"
				}
			]
		}
	]
}
```