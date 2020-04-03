#------------------------------------------------------------------------------
# Makefile - simple build commands to package up python build
#------------------------------------------------------------------------------


#-- package -------------------------------------------------------------------

package-make:
	python3 setup.py sdist bdist_wheel

package-upload:
	python3 -m twine upload dist/*

#-- test ----------------------------------------------------------------------

run-tests-py3:
	python3 -m unittest tests/test_*.py
