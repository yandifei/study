package com.yandifei.exam.service;

import com.yandifei.exam.domain.SmbmsBill;

import java.util.List;

/**
 * 订单 Service 接口
 */
public interface BillService {

    // 分页查询订单列表
    List<SmbmsBill> getBillListByPage(String productName, String proContact);

    // 查询不重复的供应商列表
    List<SmbmsBill> getDistinctBillList();

    // 添加订单
    boolean add(SmbmsBill bill);

    // 根据 ID 查询订单
    SmbmsBill getBillById(Integer id);

    // 修改订单
    boolean modify(SmbmsBill bill);

    // 删除订单
    boolean deleteBillById(Integer id);
}
