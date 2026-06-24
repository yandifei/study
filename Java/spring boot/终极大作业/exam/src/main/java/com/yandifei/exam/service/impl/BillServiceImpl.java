package com.yandifei.exam.service.impl;

import com.yandifei.exam.dao.BillMapper;
import com.yandifei.exam.domain.SmbmsBill;
import com.yandifei.exam.service.BillService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 订单 Service 实现
 */
@Service
public class BillServiceImpl implements BillService {

    @Autowired
    private BillMapper billMapper;

    @Override
    public List<SmbmsBill> getBillListByPage(String productName, String proContact) {
        return billMapper.getBillListByPage(productName, proContact);
    }

    @Override
    public List<SmbmsBill> getDistinctBillList() {
        return billMapper.getdistinctSmbmsBill();
    }

    @Override
    public boolean add(SmbmsBill bill) {
        return billMapper.add(bill) > 0;
    }

    @Override
    public SmbmsBill getBillById(Integer id) {
        return billMapper.getBillById(id);
    }

    @Override
    public boolean modify(SmbmsBill bill) {
        return billMapper.modify(bill) > 0;
    }

    @Override
    public boolean deleteBillById(Integer id) {
        return billMapper.deleteBillById(id) > 0;
    }
}
