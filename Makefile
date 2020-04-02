#------------------------------------------------------------------------------
# Makefile - simple build commands to package up python build
#------------------------------------------------------------------------------

make-package:
	python3 setup.py sdist bdist_wheel

upload-package:
	python3 -m twine upload dist/*
