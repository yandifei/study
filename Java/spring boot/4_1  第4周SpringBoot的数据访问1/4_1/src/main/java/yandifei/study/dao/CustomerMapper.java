package yandifei.study.dao;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import yandifei.study.domain.Customer;
import yandifei.study.domain.User;

import java.util.List;
@Mapper
public interface CustomerMapper {
//    @Select("select * from t_customer")
    List<Customer> findAllCustomer();
}
