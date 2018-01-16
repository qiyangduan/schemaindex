rm ./dist/schemaindex*
# touch ./schemaindex/app/do_schemaindex_init
rm ./schemaindex/allmod*
python setup.py sdist
# twine upload dist/*


