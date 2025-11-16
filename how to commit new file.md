git pull origin main --rebase

git add "Machine Learning Workflow/Data Preprocessing/data-preprocessing.ipynb"

git commit -m "Update preprocessing notebook"

git push origin main

when it says:
error: cannot pull with rebase: You have unstaged changes.

error: Please commit or stash them.

you can commit the changes like this:

git add .

git commit -m "work in progress"

git pull origin main --rebase
