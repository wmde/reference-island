# Exit script if any of the commands fail
set -e

BRANCH=$1
HOME="/data/project/wd-ref-island"

rm "$HOME/public_html/stage/$BRANCH-api.php"
echo "$BRANCH-api.php was successfully removed"