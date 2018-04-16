#!/bin/bash

project=$1
shift

# echo check if changed before building
filechanged=$(git show -q $* | wc -l)
if [ "$filechanged" -eq 0 ]; then
    SKIP_CI="No changes"
    echo "In $* changed $filechanged files, requesting a skip for ${project}"
else
    echo "In $* changed $filechanged files, possible triggering of ${project}"
fi

if [ -n "${SKIP_CI}" ]
then
    echo "skipping build cause ${SKIP_CI}";
    exit 0;
fi
mkdir ${project}
cd ${project}
git init
git config credential.helper "store --file=.git/credentials"
echo "https://${GITHUB_TOKEN}:@github.com" > .git/credentials
git remote add origin https://github.com/prometeia/${project}.git
git pull origin master
git checkout master
touch build_trigger_number
touch build_trigger_branch
echo $TRAVIS_BRANCH > build_trigger_branch
echo $TRAVIS_BUILD_NUMBER > build_trigger_number
git add --all .
git commit -m "CI ${TRAVIS_BRANCH} -- ${TRAVIS_COMMIT} "
git push origin master
echo "OK!"
cd ..
