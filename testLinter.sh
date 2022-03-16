
if [ -n "$(python3 -m autopep8 --diff --recursive src)" ]; then
	echo $(python3 -m autopep8 --diff --recursive src);
	exit 1;
fi;
