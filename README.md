# TestRunner 测试工具管理平台


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

## uwsgi

```
cp uwsgi.ini.example uwsgi.ini
# modify your config
uwsgi --ini uwsgi.ini
```

nginx conf example
```
upstream flask {
    server unix:///your_path/TestRunner/uwsgi.sock;
}


server {
    listen      8888;
    charset     utf-8;
    client_max_body_size 100M;   # adjust to taste

    location /static {
       alias /your_path/TestRunner/static;
       gzip_static on;
       expires max;
       add_header Cache-Control public;
    }

    location / {
        uwsgi_pass  flask;
        include     uwsgi_params;
    }
}
```


## deploy

install node
npm install -g less
```bash
fab deploy

# 部署目录
../shared 文件夹内如大致如下
fab deploy 前
config.py uwsgi.ini venv

fab deploy 后
config.py  static  uwsgi.ini  uwsgi.log  uwsgi.pid  uwsgi.sock  venv
```


## Pycharm
```
mark src as source root
```