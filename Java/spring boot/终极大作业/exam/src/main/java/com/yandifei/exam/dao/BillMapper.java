package com.yandifei.exam.dao;

import com.yandifei.exam.domain.SmbmsBill;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 订单 Mapper 接口
 */
public interface BillMapper {

    // 分页查询订单列表（带供应商关联 + 条件搜索）
    List<SmbmsBill> getBillListByPage(@Param("productName") String productName,
                                       @Param("proContact") String proContact);

    // 查询不重复的供应商列表（用于订单搜索下拉框）
    List<SmbmsBill> getdistinctSmbmsBill();

    // 添加订单
    int add(SmbmsBill bill);

    // 根据 ID 查询订单
    SmbmsBill getBillById(@Param("id") Integer id);

    // 修改订单
    int modify(SmbmsBill bill);

    // 删除订单
    int deleteBillById(@Param("id") Integer id);
}
