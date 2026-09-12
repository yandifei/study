package yandifei.study.domain;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import yandifei.study.dao.CustomerMapper;

import java.util.List;

@SpringBootTest
class CustomerTest {
    @Autowired
    private CustomerMapper customerMapper;

    @Test
    void testFindAllCustomer() {
        List<Customer> customers = customerMapper.findAllCustomer();
        for (Customer c : customers) {
            System.out.println("ID: " + c.getId() +
                    " 姓名: " + c.getUsername() +
                    " 职业: " + c.getJobs() +
                    " 电话: " + c.getPhone());
        }
    }
}