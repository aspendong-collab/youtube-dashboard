#!/bin/bash
# 保护 requirements.txt 的脚本
# 防止自动修改 requirements.txt 为 144 行

REQUIREMENTS_FILE="requirements.txt"
CORRECT_LINES=4
CURRENT_LINES=$(wc -l < "$REQUIREMENTS_FILE")

echo "检查 requirements.txt..."
echo "当前行数: $CURRENT_LINES"
echo "预期行数: $CORRECT_LINES"

if [ "$CURRENT_LINES" -ne "$CORRECT_LINES" ]; then
    echo "⚠️  检测到 requirements.txt 被意外修改！"
    echo "当前行数: $CURRENT_LINES (应该是 $CORRECT_LINES)"
    echo "正在恢复正确的版本..."
    
    # 恢复正确的 4 行版本
    cat > "$REQUIREMENTS_FILE" << 'EOF'
streamlit==1.53.1
pandas==2.3.3
plotly==6.5.2
requests==2.32.5
EOF
    
    echo "✅ requirements.txt 已恢复为 4 行"
    
    # 如果有 Git 仓库，检查是否需要提交
    if [ -d ".git" ]; then
        if git diff --quiet "$REQUIREMENTS_FILE"; then
            echo "✅ Git 工作区干净，无需提交"
        else
            echo "⚠️  Git 检测到更改"
            git add "$REQUIREMENTS_FILE"
            echo "已暂存 requirements.txt，请提交更改"
        fi
    fi
else
    echo "✅ requirements.txt 正常 ($CURRENT_LINES 行)"
fi
