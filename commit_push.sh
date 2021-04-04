### to add, commit and push the files/folders in the argument
### first arg is commit message
### remaining are file/folder names

message="$1"

git add ${@: 2}
git commit -m message 
git push -v origin master

