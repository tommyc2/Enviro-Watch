#!/bin/bash

echo ""
echo "===================================="
echo "Installing necessary dependencies"
echo "===================================="
echo ""

while IFS= read -r LINE; do
    start=`date +%s`
    pip install $LINE
    echo $LINE
    end=`date +%s`
    runtime=$((end-start))
    echo "Installed $LINE (took $runtime seconds)"
done < requirements.txt

echo ""
echo "===================================="
echo "Done installing necessary libraries"
echo "===================================="
echo ""

echo "Run 'main.py' to start project!"