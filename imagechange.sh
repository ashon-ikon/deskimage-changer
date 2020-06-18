#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PULL_NEW_IMAGE=
SCRIPT_NAME="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"

function pull_new_images {
	if [ -z "${PULL_NEW_IMAGE}" ]; then
		return
	fi
	OLD_DIR=$(pwd)
	cd "${CURRENT_DIR}"
	echo " Pulling new wallpaper..."
	("${CURRENT_DIR}/deskimage.py" > /dev/null 2>&1 )
	cd "${OLD_DIR}"
	echo "   done."
}

function change_image {
	PIC=$(find "${CURRENT_DIR}/" -name '*landscape*.jpg' | shuf -n1)
	echo " ... Changing wallpaper to ${PIC}"
	gsettings set org.gnome.desktop.background picture-uri "file://${PIC}"
	echo "  Done"
}

function show_usage {
        echo "Run script as "
        echo "    ${SCRIPT_NAME} [-n|--new] "
        echo ""
        echo " -n | --new  : Attempt to pull new image while chaning the desktop image"
        echo ""
        echo " -h | --help : To see this usage info"
        echo ""
        echo "Check \`${CURRENT_DIR}' for copyright of each image."
        echo ""
        echo "      ... Have fun!"
}


function parse_args {
	while [ "$1" != "" ]; do
		case $1 in
			-n | --new ) shift
				PULL_NEW_IMAGE=1
				;;
			-h | --help ) show_usage
				exit
				;;
			* ) show_usage
				exit 1
		esac
		shift
	done
}


function run_service {
	parse_args "$@"
	pull_new_images
	change_image
}


run_service "$@"
