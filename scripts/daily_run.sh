scripts_dir=$(dirname $(readlink -f $0))
root_dir=$(dirname $scripts_dir)
VENV_NAME=".daily_venv"
VENV_PATH="${scripts_dir}/../${VENV_NAME}"
PYTHON="${VENV_PATH}/bin/python"

$PYTHON root_dir/src/main.py "$@"
