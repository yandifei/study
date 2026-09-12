package com.my.dao;

import com.my.pojo.Person;

import java.util.List;

public interface PersonMapper {
    public List<Person> findPersonById(int id);
}