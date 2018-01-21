rm ./dist/schemaindex*
# touch ./schemaindex/app/do_schemaindex_init
mv ./schemaindex/schemaindex.sqlite3 /tmp/schemaindex.sqlite3.tmp
python setup.py sdist
mv /tmp/schemaindex.sqlite3.tmp  ./schemaindex/schemaindex.sqlite3
# twine upload dist/*


