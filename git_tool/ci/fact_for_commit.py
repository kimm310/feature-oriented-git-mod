from prompt_toolkit import PromptSession
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.widgets import TextArea
import git

# Git-Repository initialisieren
repo = git.Repo(".")

# Git-History abrufen
commits = list(repo.iter_commits("main", max_count=100))

# Erstelle eine Liste von Commit-Details
commit_details = []
for commit in commits:
    details = {
        "id": commit.hexsha,
        "message": commit.message.strip(),
        "date": commit.committed_datetime,
        "files": commit.stats.files,
    }
    commit_details.append(details)

# Initialisiere den Index für die Commit-Auswahl
current_index = 0


# Funktion zum Aktualisieren des Textes basierend auf dem aktuellen Index
def get_commit_text(index):
    commit = commit_details[index]
    file_list = "\n".join(commit["files"].keys())
    return (
        f"Commit ID: {commit['id']}\n"
        f"Date: {commit['date']}\n"
        f"Message: {commit['message']}\n"
        f"Files:\n{file_list}"
    )


# TextArea für die Anzeige der Commit-Details
commit_text_area = TextArea(text=get_commit_text(current_index), read_only=True)

# Key Bindings definieren
kb = KeyBindings()


@kb.add("up")
def up(event):
    global current_index
    if current_index > 0:
        current_index -= 1
        commit_text_area.text = get_commit_text(current_index)


@kb.add("down")
def down(event):
    global current_index
    if current_index < len(commit_details) - 1:
        current_index += 1
        commit_text_area.text = get_commit_text(current_index)


@kb.add("enter")
def select_commit(event):
    commit = commit_details[current_index]
    print(f'Selected Commit ID: {commit["id"]}')
    event.app.exit()


# Layout und Anwendung erstellen
layout = Layout(HSplit([commit_text_area]))

application = Application(layout=layout, key_bindings=kb, full_screen=True)

# Anwendung ausführen
if __name__ == "__main__":
    application.run()
