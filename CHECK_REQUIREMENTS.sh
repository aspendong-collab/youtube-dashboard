#!/bin/bash
# Script to verify requirements.txt is correct

echo "Checking requirements.txt..."
echo ""

lines=$(wc -l < requirements.txt)

if [ "$lines" -gt 5 ]; then
    echo "❌ ERROR: requirements.txt has $lines lines (should be 4)"
    echo ""
    echo "Current content:"
    head -10 requirements.txt
    echo "..."
    tail -5 requirements.txt
    echo ""
    echo "Expected content:"
    cat << 'EXPECTED'
streamlit==1.53.1
pandas==2.3.3
plotly==6.5.2
requests==2.32.5
EXPECTED
    echo ""
    echo "Fixing requirements.txt..."
    cat > requirements.txt << 'EOF'
streamlit==1.53.1
pandas==2.3.3
plotly==6.5.2
requests==2.32.5
