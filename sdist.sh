rm ./dist/schemaindex*
# touch ./schemaindex/app/do_schemaindex_init
# rm ./schemaindex/schemaindex.sqlite3
python setup.py sdist
# twine upload dist/*


