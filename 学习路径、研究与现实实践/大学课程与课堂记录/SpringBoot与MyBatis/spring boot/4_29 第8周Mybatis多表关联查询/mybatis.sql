/*
SQLyog v10.2 
MySQL - 5.6.17 : Database - mybatis
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`mybatis` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `mybatis`;

/*Table structure for table `t_customer` */

DROP TABLE IF EXISTS `t_customer`;

CREATE TABLE `t_customer` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `jobs` varchar(50) DEFAULT NULL,
  `phone` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `t_customer` */

insert  into `t_customer`(`id`,`username`,`jobs`,`phone`) values (1,'joy','teacher','13733333333'),(2,'jack','teacher','13522222222'),(3,'tom','worker','15111111111');

/*Table structure for table `t_student` */

DROP TABLE IF EXISTS `t_student`;

CREATE TABLE `t_student` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `sname` varchar(50) DEFAULT NULL,
  `sage` int(11) DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `t_student` */

insert  into `t_student`(`sid`,`sname`,`sage`) values (1,'Lucy',25),(2,'Lili',20),(3,'Jim',20);

/*Table structure for table `tb_class` */

DROP TABLE IF EXISTS `tb_class`;

CREATE TABLE `tb_class` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classname` varchar(20) DEFAULT NULL,
  `grade` varchar(20) DEFAULT NULL,
  `headmaster` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `tb_class` */

insert  into `tb_class`(`id`,`classname`,`grade`,`headmaster`) values (1,'计算机1班','20','张小平');

/*Table structure for table `tb_idcard` */

DROP TABLE IF EXISTS `tb_idcard`;

CREATE TABLE `tb_idcard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CODE` varchar(18) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `tb_idcard` */

insert  into `tb_idcard`(`id`,`CODE`) values (1,'152221198711020624'),(2,'152201199008150317');

/*Table structure for table `tb_order` */

DROP TABLE IF EXISTS `tb_order`;

CREATE TABLE `tb_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `productname` varchar(30) DEFAULT NULL,
  `price` decimal(10,0) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

/*Data for the table `tb_order` */

insert  into `tb_order`(`id`,`productname`,`price`,`number`,`userid`) values (1,'橄榄油','20',20,1),(2,'洗洁精','15',10,1),(3,'塑料杯','2',100,1),(4,'泰国香米','60',2,2),(5,'可口可乐','3',10,2),(6,'美国大杏仁','10',5,2),(7,'葡萄酒','6',10,3),(8,'豆瓣酱','4',2,3);

/*Table structure for table `tb_password` */

DROP TABLE IF EXISTS `tb_password`;

CREATE TABLE `tb_password` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(20) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `uid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

/*Data for the table `tb_password` */

insert  into `tb_password`(`id`,`password`,`role`,`uid`) values (1,'123456','管理员',1),(2,'222223','普通用户',2),(3,'333333','普通用户',3),(4,'534346','普通用户',4),(5,'777777','管理员',5),(6,'888888','普通用户',6);

/*Table structure for table `tb_person` */

DROP TABLE IF EXISTS `tb_person`;

CREATE TABLE `tb_person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `sex` varchar(8) DEFAULT NULL,
  `card_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_id` (`card_id`),
  CONSTRAINT `tb_person_ibfk_1` FOREIGN KEY (`card_id`) REFERENCES `tb_idcard` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `tb_person` */

insert  into `tb_person`(`id`,`name`,`age`,`sex`,`card_id`) values (1,'Rose',22,'女',1),(2,'jack',23,'男',2);

/*Table structure for table `tb_score` */

DROP TABLE IF EXISTS `tb_score`;

CREATE TABLE `tb_score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coursename` varchar(20) DEFAULT NULL,
  `score` decimal(10,0) DEFAULT NULL,
  `studentid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

/*Data for the table `tb_score` */

insert  into `tb_score`(`id`,`coursename`,`score`,`studentid`) values (1,'体育','90',1),(2,'网页设计','85',1),(3,'美术','88',1),(4,'体育','76',2),(5,'网页设计','91',2),(6,'美术','88',2),(7,'体育','89',3),(8,'网页设计','78',3),(9,'美术','87',3);

/*Table structure for table `users` */

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `uname` varchar(20) DEFAULT NULL,
  `uage` int(11) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

/*Data for the table `users` */

insert  into `users`(`uid`,`uname`,`uage`) values (1,'张三',20),(2,'李四',18),(3,'王国',22),(4,'陈述',23),(5,'周围',22);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
