PYTHON="/usr/bin/python3.7"

scripts_dir=$(dirname $(readlink -f $0))

VENV_NAME=".daily_venv"
VENV_PATH="${scripts_dir}/../${VENV_NAME}"
if [ -d ${VENV_PATH} ]; then
  echo "virtual environment already exists"
else
    cd ${scripts_dir}/../ || exit 1
    VENV_PATH="${scripts_dir}/../${VENV_NAME}"
    ${PYTHON} -m venv --without-pip ${VENV_NAME}

    curl https://bootstrap.pypa.io/get-pip.py | ${VENV_PATH}/bin/python

    PIP="${VENV_PATH}/bin/pip"

    ${PIP} install --upgrade pip

    sh ${scripts_dir}/install_requirements.sh $VENV_NAME
fi
