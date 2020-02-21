VENV='.daily_venv'
scripts_dir=$(dirname $(readlink -f $0))
echo "Create virtual environment"
cd $scripts_dir || exit 1
sh create_venv.sh

echo "Create work directory"
cd $scripts_dir/.. || exit 1
$VENV/bin/python src/install.py $1




