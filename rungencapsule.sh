#!/bin/bash

# 检查参数
if [ $# -ne 2 ]; then
    echo "用法: $0 <basename> <git_path>"
    echo "示例: $0 example /path/to/git/repo"
    exit 1
fi

# 获取参数
BASENAME="$1"
GIT_PATH="$2"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 虚拟环境路径
VENV_PATH="${SCRIPT_DIR}/venv"

# gencapsule.py 路径
GENCAPSULE_SCRIPT="${SCRIPT_DIR}/gencapsule.py"

# 检查虚拟环境是否存在
if [ ! -d "$VENV_PATH" ]; then
    echo "错误: 虚拟环境不存在: $VENV_PATH"
    exit 1
fi

# 检查 gencapsule.py 是否存在
if [ ! -f "$GENCAPSULE_SCRIPT" ]; then
    echo "错误: gencapsule.py 不存在: $GENCAPSULE_SCRIPT"
    exit 1
fi

# 激活虚拟环境
source "$VENV_PATH/bin/activate"

# 检查虚拟环境是否成功激活
if [ $? -ne 0 ]; then
    echo "错误: 无法激活虚拟环境: $VENV_PATH"
    exit 1
fi

echo "已激活虚拟环境: $VENV_PATH"
echo "正在运行: python $GENCAPSULE_SCRIPT $BASENAME $GIT_PATH"

# 设置环境变量
export GENCAPSULE_BASE_DIR="$GIT_PATH"

# 运行 gencapsule.py
python "$GENCAPSULE_SCRIPT" "$BASENAME" "$GIT_PATH"

# 获取返回码
EXIT_CODE=$?

# 取消激活虚拟环境
deactivate

# 返回 gencapsule.py 的退出码
exit $EXIT_CODE 