#!/bin/bash
# Check whether a git repo is in a branch
# Useful for when using a shared system with (say) a puppetmaster with
# a central repo that people might branch in order to test
# changes. Best used in .bashrc/.bash_logout files or what have you.

function check_repo {
    branch_head=$(cat $1/.git/HEAD)
    current_branch=${branch_head##*/}
    if [ $current_branch != "master" ]; then
	echo "WARNING: $1 is in branch $current_branch!";
    fi
}

check_repo $1
