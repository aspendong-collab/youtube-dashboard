#!/bin/bash
echo "Checking requirements.txt..."
lines=$(wc -l < requirements.txt)

if [ "$lines" -gt 5 ]; then
    echo "ERROR: requirements.txt has $lines lines (should be 4)"
    echo "Fixing..."
    cat > requirements.txt << 'EOF'
streamlit==1.53.1
pandas==2.3.3
plotly==6.5.2
requests==2.32.5
EOF
    echo "Fixed!"
else
    echo "OK: requirements.txt has $lines lines"
fi
