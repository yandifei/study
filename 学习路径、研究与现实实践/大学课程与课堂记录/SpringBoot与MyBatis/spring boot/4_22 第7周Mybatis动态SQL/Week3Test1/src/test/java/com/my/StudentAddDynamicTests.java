package com.my;

import com.my.domain.Student;
import com.my.service.StudentService;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

/**
 * 测试 Student 动态添加功能（动态SQL）
 * 验证只插入用户实际填写的字段，未填写的字段在数据库中为 NULL
 */
@SpringBootTest
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)  // 按顺序执行测试
public class StudentAddDynamicTests {

    @Autowired
    private StudentService studentService;

    /**
     * 测试1：只提供姓名，不提供年龄
     * 预期：数据库新增一条记录，sname 有值，sage 为 NULL
     */
    @Test
    @Order(1)
    public void testAddStudent_OnlyName() {
        System.out.println("========== 测试1：只提供姓名 ==========");
        Student student = new Student();
        student.setSname("动态测试-只姓名");
        // 不设置年龄

        int count = studentService.addStudentDynamic(student);
        if (count > 0) {
            System.out.println("添加成功！插入记录数：" + count);
            System.out.println("请检查数据库 t_student 表，应有一条 sname='动态测试-只姓名'，sage 为 NULL 的记录");
        } else {
            System.out.println("添加失败！");
        }
        System.out.println();
    }

    /**
     * 测试2：只提供年龄，不提供姓名
     * 预期：数据库新增一条记录，sname 为 NULL，sage 有值
     */
    @Test
    @Order(2)
    public void testAddStudent_OnlyAge() {
        System.out.println("========== 测试2：只提供年龄 ==========");
        Student student = new Student();
        student.setSage(21);
        // 不设置姓名

        int count = studentService.addStudentDynamic(student);
        if (count > 0) {
            System.out.println("添加成功！插入记录数：" + count);
            System.out.println("请检查数据库 t_student 表，应有一条 sname 为 NULL，sage=21 的记录");
        } else {
            System.out.println("添加失败！");
        }
        System.out.println();
    }

    /**
     * 测试3：姓名和年龄都提供
     * 预期：数据库新增一条记录，两个字段都有值
     */
    @Test
    @Order(3)
    public void testAddStudent_BothNameAndAge() {
        System.out.println("========== 测试3：姓名和年龄都提供 ==========");
        Student student = new Student();
        student.setSname("动态测试-全填");
        student.setSage(22);

        int count = studentService.addStudentDynamic(student);
        if (count > 0) {
            System.out.println("添加成功！插入记录数：" + count);
            System.out.println("请检查数据库 t_student 表，应有一条 sname='动态测试-全填'，sage=22 的记录");
        } else {
            System.out.println("添加失败！");
        }
        System.out.println();
    }

    /**
     * 测试4：姓名和年龄都不提供（空对象）
     * 预期：数据库新增一条记录，sname 和 sage 均为 NULL
     * 注意：这依赖于表结构允许字段为 NULL，否则会报错
     */
    @Test
    @Order(4)
    public void testAddStudent_EmptyObject() {
        System.out.println("========== 测试4：姓名和年龄都不提供 ==========");
        Student student = new Student();
        // 不设置任何属性

        int count = studentService.addStudentDynamic(student);
        if (count > 0) {
            System.out.println("添加成功！插入记录数：" + count);
            System.out.println("请检查数据库 t_student 表，应有一条 sname 和 sage 均为 NULL 的记录");
        } else {
            System.out.println("添加失败！");
        }
        System.out.println();
    }

    /**
     * 测试5：姓名为空字符串，年龄有值
     * 预期：空字符串等同于不提供（因为动态SQL判断 sname != null and sname != ''）
     *       最终 sname 应为 NULL（数据库默认），sage 有值
     */
    @Test
    @Order(5)
    public void testAddStudent_EmptyStringName() {
        System.out.println("========== 测试5：姓名为空字符串，年龄有值 ==========");
        Student student = new Student();
        student.setSname("");   // 空字符串
        student.setSage(23);

        int count = studentService.addStudentDynamic(student);
        if (count > 0) {
            System.out.println("添加成功！插入记录数：" + count);
            System.out.println("预期：sname 为 NULL，sage=23。请验证数据库。");
        } else {
            System.out.println("添加失败！");
        }
        System.out.println();
    }

    /**
     * 测试6：姓名为 null，年龄有值（显式设置 null）
     * 预期：效果同测试2
     */
    @Test
    @Order(6)
    public void testAddStudent_NullName() {
        System.out.println("========== 测试6：姓名为 null，年龄有值 ==========");
        Student student = new Student();
        student.setSname(null);
        student.setSage(24);

        int count = studentService.addStudentDynamic(student);
        if (count > 0) {
            System.out.println("添加成功！插入记录数：" + count);
            System.out.println("预期：sname 为 NULL，sage=24。请验证数据库。");
        } else {
            System.out.println("添加失败！");
        }
        System.out.println();
    }

    /**
     * 汇总测试：连续执行以上所有测试，结束后打印提示信息
     */
    @Test
    @Order(7)
    public void printSummary() {
        System.out.println("========================================");
        System.out.println("所有测试执行完毕！");
        System.out.println("请打开数据库管理工具，执行以下 SQL 查看新增记录：");
        System.out.println("SELECT * FROM t_student WHERE sname LIKE '动态测试%' OR sname IS NULL ORDER BY sid DESC LIMIT 10;");
        System.out.println("========================================");
    }
}