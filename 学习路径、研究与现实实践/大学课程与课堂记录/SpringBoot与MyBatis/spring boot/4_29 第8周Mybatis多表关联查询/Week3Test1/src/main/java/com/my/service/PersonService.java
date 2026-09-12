package com.my.service;

import com.my.pojo.Person;
import java.util.List;

public interface PersonService {
    /**
     * 根据ID查询人员及其关联的身份证信息 (一对一)
     */
    public List<Person> findPersonById(int id);
}