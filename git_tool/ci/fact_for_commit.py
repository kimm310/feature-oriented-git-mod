if __name__ == "__main__":
    import os
    import sys

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
from datetime import datetime
from git_tool.feature_data.add_data import add_fact_to_metadata_branch
from git_tool.feature_data.fact_model import ChangeHolder, FeatureFactModel
from git_tool.feature_data.repo_context import repo_context


features = {"Feature A": "uuid-1", "Feature B": "uuid-2", "Feature C": "uuid-3"}

from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt


def select_features(features):
    choices = [(uuid, name) for name, uuid in features.items()]
    selected = []

    print("Select features (use space to toggle, enter to confirm):")
    while True:
        print(selected)
        for i, (uuid, name) in enumerate(choices):
            selected_marker = "[x]" if uuid in selected else "[ ]"
            print(f"{i + 1}. {selected_marker} {name}")

        selection = prompt("> ")

        if selection.isdigit():
            index = int(selection) - 1
            if 0 <= index < len(choices):
                uuid, name = choices[index]
                if uuid in selected:
                    selected.remove(uuid)
                else:
                    selected.append(uuid)
        elif selection.lower() in ("done", "d"):
            break
        else:
            print(
                "Invalid selection. Enter the number of the feature to toggle selection, or 'done' to finish."
            )

    return selected


if __name__ == "__main__":
    commit_id = input("Enter Commit Id:")
    with repo_context() as repo:
        commit = repo.commit(commit_id)
        print(commit, commit.message)
    selected_uuid = select_features(features)
    fact = FeatureFactModel(
        commit=str(commit),
        authors=[commit.author.name],
        date=datetime.now(),
        feature=selected_uuid,
        changes=ChangeHolder(
            code_changes=[], constraint_changes=[], name_change=None
        ),
    )
    add_fact_to_metadata_branch(fact=fact, commit_ref=commit)
