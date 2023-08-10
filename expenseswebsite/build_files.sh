echo " BUILD START"
python3.9 -m pip install -r requirements.txt

echp "Make Migrations"
python 3.9 manage.py makemigrations --noinput
python 3.9 manage.py migrate
python3.9 manage.py collectstatic --noinput --clear
echo " BUILD END"  
