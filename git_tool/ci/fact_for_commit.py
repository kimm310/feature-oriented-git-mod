if __name__ == "__main__":
    import os
    import sys

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
from datetime import datetime

from prompt_toolkit import prompt

from git_tool.feature_data.add_feature_data.add_data import (
    add_fact_to_metadata_branch,
)
from git_tool.feature_data.models_and_context.fact_model import (
    ChangeHolder,
    FeatureFactModel,
)
from git_tool.feature_data.models_and_context.repo_context import repo_context


# TODO currently unused code
def select_features(feature_options: dict[str, str]) -> list:
    """
    Let users decide which features to use by selection.
    """
    choices = [(uuid, name) for name, uuid in feature_options.items()]
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
    # selected_uuid = select_features(features)
    features = ["test"]
    fact = FeatureFactModel(
        commit=str(commit),
        authors=[commit.author.name],
        date=datetime.now(),
        features=features,
        changes=ChangeHolder(
            code_changes=[], constraint_changes=[], name_change=None
        ),
    )
    add_fact_to_metadata_branch(fact=fact, commit_ref=commit)
