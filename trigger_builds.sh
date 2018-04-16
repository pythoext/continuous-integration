#!/bin/bash

# echo check if changed before building
filechanged=$(git show -q $2 | wc -l)
if [ "$filechanged" -eq 0 ]; then
    SKIP_CI="SKIUS"
    echo "In $2 changed $filechanged files, requesting a skip"
else
    echo "In $2 changed $filechanged files, triggering $1"
fi

if [ -n "${SKIP_CI}" ]
then
    echo "skipping build";
    exit 0;
fi
mkdir $1
cd $1
git init
git config credential.helper "store --file=.git/credentials"
echo "https://${GITHUB_TOKEN}:@github.com" > .git/credentials
git remote add origin https://github.com/prometeia/$1.git
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
