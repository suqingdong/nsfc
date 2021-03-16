find . -name __pycache__ -exec rm -rf {} \;

rm -rf *.egg-info build dist

python3 setup.py sdist bdist_wheel
