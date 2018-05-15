#TestRunner 测试工具管理平台


## install packages

## install virtualenv

```bash
easy_install pip
pip install virtualenv
cd treasure
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
# or use mirror
# pip install --index https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt

# 退出venv环境
deactivate
```


## development

```
cp src/app/config.py.example src/app/config.py
cp src/jobs/schedule.py.example src/jobs/schedule.py
source venv/bin/activate
cd src && python manage.py db upgrade && cd ..
python src/manage.py runserver

# open http://127.0.0.1:5000/ in your browser

## start celery worker
cd src && celery -A jobs worker

## start celery schedule
cd src &&  celery -A jobs beat
```


# Pycharm
```
mark src as source root
```