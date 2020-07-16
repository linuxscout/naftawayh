#/usr/bin/sh
# Build Naftawayh: Arabic word tagger package

default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all: install install3 wheel wheel3  doc
install:
	sudo python setup.py install
install3:
	sudo python3 setup.py install
# Publish to github
publish:
	git push origin master 

md2rst:
	pandoc -s -r markdown -w rst README.md -o README.rst
md2html:
	pandoc -s -r markdown -w html README.md -o README.html
	
wheel:
	sudo python setup.py bdist_wheel
wheel3:
	sudo python3 setup.py bdist_wheel
sdist:
	sudo python setup.py sdist
upload:
	echo "use twine upload dist/naftawayh-0.3.tar.gz"
	
test:
	python -m unittest discover tests
test3:
	cd tests;python3 -m unittest discover tests
doc:
	epydoc --config epydoc.conf
