# PURPOSE: Generate emags TAGS files,
# for jumping to the definition of a symbol (usually a function).

# PITFALL: This calls the `etags_plus` script,
# which is defined in another repo:
# git@github.com:JeffreyBenjaminBrown/play.git
# where it is called `etags+.sh`.

find . -name "*.py" | grep -v "/migrations/" | xargs ~/bash/etags_plus.sh
