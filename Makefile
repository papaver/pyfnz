#------------------------------------------------------------------------------
# Makefile - simple build commands to package up python build
#------------------------------------------------------------------------------


#-- package -------------------------------------------------------------------

make-package:
	python3 setup.py sdist bdist_wheel

upload-package:
	python3 -m twine upload dist/*

#-- test ----------------------------------------------------------------------

run-tests-py3:
	python3 -m unittest tests/test_*.py
