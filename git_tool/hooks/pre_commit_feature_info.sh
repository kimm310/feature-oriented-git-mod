#!/bin/sh

# Prompt the user for feature information
echo "Please enter feature information for this commit:"
read feature_info

# Save the feature information to a temporary file
# echo "$feature_info" > .git/hooks/feature_info.txt

# Alternatively, you can add it as a commit message trailer
echo "Feature-Info: $feature_info" >> "$(git rev-parse --git-dir)/COMMIT_EDITMSG"

# Allow the commit to proceed
exit 0
