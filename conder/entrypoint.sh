#!/bin/bash
set -e

if [ "$1" = 'BOOTSTRAP' ]; then
    cd /conder
    bash update-offline-repo.sh  $DISTRO $TOKEN $REPO $APPLICATIONS
else
    $@
fi
