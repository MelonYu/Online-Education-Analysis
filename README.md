# Online-Education-Analysis

[TOC]

## 1. IMOOC

爬虫基础测试

练习类和对象编程，pymysql的使用

### 1.1 需求分析

### 1.2 数据库设计

**a. freecourse**  

id, course_url, image_url, course_label, course_name, course_grade, course_population, course_desc

```mysql
CREATE TABLE free_course_info(
    id SMALLINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    course_url VARCHAR(40) NOT NULL,
    image_url VARCHAR(70) NOT NULL,
    course_label VARCHAR(50) NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    course_grade VARCHAR(10) NOT NULL,
    course_population MEDIUMINT UNSIGNED,
    course_desc VARCHAR(255)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

```



