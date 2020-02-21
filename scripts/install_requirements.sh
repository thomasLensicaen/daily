VENV_NAME=$1

scripts_dir=$(dirname $(readlink -f $0))
cd ${scripts_dir}/../

VENV_PATH="${scripts_dir}/../${VENV_NAME}"

PIP="${VENV_PATH}/bin/pip"

${PIP} install -r scripts/requirements.txt
