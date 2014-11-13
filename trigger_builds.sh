#!/bin/bash

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
git commit -m "Automated push to trigger a new build"
git push origin master
echo "OK!"
cd ..