# LuffyManageBackend

Thank you to all the people who already contributed to luffycity's project！

---

## Introduction

这是一个使用 `django` 实现的偏管理的后台，涉及路飞整体业务中的三个业务板块，以下是它们的介绍及站点访问地址：

**管理后台(内网)**

[管理站点](http://192.168.0.8/manage/) 是为路飞运营人员所提供的日常运营数据展示及处理的站点。

**导师后台(外网)**

[导师站点](http://mentor.luffycity.com/mentor/) 是为路飞导师所提供的管理学员的站点。

**CRM后台(外网)**

[CRM站点](http://crm.luffyctiy.com/crm/) 是为路飞课程顾问所提供的管理客户的站点。

## Basic Environmental

- Python3.6.8  
- Mysql5.7.x  
- Redis3.0  
- Celery4.2.x  
- Git    

## Getting Started

**Installation**

```
pip3 install virtualenv

// macos & linux 环境下
virtualenv env
source env/bin/activate

// install packages
pip install -r requirements.txt

// checkout your branch
git checkout -b YOUR-USERNAME
```

**Config your settings**

```
// 在项目目录下创建 `local_settings.py` 
// 将你的数据库及缓存配置添加到该文件中
```

## Quick Tutorial  

**Start Project**

```
python manage.py makemigrations
python manage.py migrate

// 创建超级用户
python manage.py createsuperuser

// 启动
python manage.py runserver 0.0.0.0:8000
```

**Start Celery**

```
// 启动 worker
celery -A otherDemo worker -l info

// 启动 celery beat 
celery -A otherDemo beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

// 启动 celery 监控, 生产环境建议内网访问
python3 manage.py flower 
```

## Q&A

> 创建数据库的时候，可能出现MySQL的字符集的问题

```
CREATE DATABASE luffy_dev DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

## Support

```
2019 By luffycity devlpers.
```
