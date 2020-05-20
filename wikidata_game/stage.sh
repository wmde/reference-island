# Exit script if any of the commands fail
set -e

BRANCH=$1
HOME="/data/project/wd-ref-island"

git -C "$HOME/reference-island/" fetch --all
git -C "$HOME/reference-island/" checkout $BRANCH
git -C "$HOME/reference-island/" pull

if [ ! -d "$HOME/public_html/stage" ]; then
    mkdir "stage"
fi

cp "$HOME/reference-island/wikidata_game/api.php" "$HOME/public_html/stage/$BRANCH-api.php"
echo "$BRANCH-api.php updated successfuly"