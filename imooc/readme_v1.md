# IMOOC 网页爬取流程

[TOC]

## 1. 爬取的内容

https://www.imooc.com

### 1.1 免费课程

#### a. 免费课程列表 (freecourse.py)

按热度从高到低：
https://www.imooc.com/course/list?sort=pop&page=[1,36] # 具体的页数会变的

| 名称          | 变量名         | 示例 |
| ------------- | -------------- | ---- |
| 课程的url     | course_url     |      |
| 课程题图的url | course_img_url |      |
| 课程分类      | course_tags    |      |
| 课程名称      | course_name    |      |
| 课程等级      | course_grade   |      |
| 课程人数      | course_pp      |      |
| 课程描述      | course_desc    |      |

#### b. 免费课程详情页 (test_courseinfodetail.py)

**主页面**

| 名称         | 变量名            | 示例 |
| ------------ | ----------------- | ---- |
| 课程访问路径 | course_path       |      |
| 课程须知     | course_tip_first  |      |
| 能学到什么   | course_tip_second |      |
| 教师姓名     | teacher_name      |      |
| 教师页面url  | teacher_url       |      |
| 教师职业     | teacher_job       |      |
| 课程时长     | course_duration   |      |
| 课程评分     | course_score      |      |
| 问答评论人数 | comment_pp        |      |
| 参与评价人数 | score_pp          |      |

后续可以增加：

**课程章节**

章节具体名称；章节的类型；章节的具体时长；章节对应的url

**问答评论**

**用户评价**

**实现课程视频自动下载，按章节拼接等功能**

### 1.2 用户页

#### a. 用户基本数据 (test_userdetail.py)

| 名称          | 变量名         | 示例 |
| ------------- | -------------- | ---- |
|用户名|user_name|weibo_借我时间_0|
|性别|sex|男|
|头像url|user_pic_url|//img1.mukewang.com/56xxxx-140.jpg|
|个人签名|user_sign|行动胜过一切！|
|省份|province|四川|
|城市|city|成都市|
|职业|career|学生|
|学习时长|total_study_duration|628h|
|经验|exp|18160|
|积分|coins|39|
|关注|follows|1|
|粉丝|fans|0|

数据库

user_basic_info

```mysql
CREATE TABLE user_basic_info(
    id SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNSIGNED,
    user_name VARCHAR(40) NOT NULL,
    sex VARCHAR(10) NOT NULL,
    user_pic_url VARCHAR(100) NOT NULL,
    user_sign VARCHAR(100),
    province VARCHAR(20),
    city VARCHAR(20),
    career VARCHAR(20) ,
    total_study_duration VARCHAR(10),
    exp INT UNSIGNED,
    coins INT UNSIGNED,
	follows INT UNSIGNED,
    fans INT UNSIGNED
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



#### b.用户学习课程情况 (test_userdetail.py)

| 名称          | 变量名         | 示例 |
| ------------- | -------------- | ---- |
|课程ID(url)|course_url|/learn/369|
|课程名称|course_name|Oracle数据库开发必备利器之SQL基础|
|最近学习时间|recent_study_date|2018年06月11日|
|已学|has_learn|7%|
|花费时长|time_consuming|用时 6小时55分|
|学至|study_to|学习至2-1 使用系统用户登录Oracle|
|笔记数|note_num|0|
|代码数|code_num|0|
|问答数|ques_num|0|

数据库：

user_learn_detail

```mysql
CREATE TABLE user_learn_detail(
    id SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNSIGNED NOT NULL,
    course_url VARCHAR(20) NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    recent_study_date VARCHAR(30) NOT NULL,
    has_learn VARCHAR(5) NOT NULL,
    time_consuming VARCHAR(30),
    study_to VARCHAR(100),
    note_num INT UNSIGNED,
    code_num INT UNSIGNED,
    ques_num INT UNSIGNED
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



## 2. 多线程爬取，并存入MySQL

### 2.1  多线程爬取方案

### 2.2 数据库设计

### 2.3 具体实现


## 3. 数据分析方案

### 3.1 课程的构成特点

- 各个分类的课程的数量


## 4. 数据展示方案

使用vue.js + highcharts(or echarts) 等做一个简单的展示页面。