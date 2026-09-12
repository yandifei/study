package com.my.service;

import com.my.dao.PersonMapper;
import com.my.pojo.Person;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PersonServiceImpl implements PersonService {

    @Autowired
    private PersonMapper personMapper;

    @Override
    public List<Person> findPersonById(int id) {
        System.out.println("正在通过Service层查询人员信息，ID为: " + id);
        return personMapper.findPersonById(id);
    }
}