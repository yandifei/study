package com.yandifei.exam.service;

import com.yandifei.exam.domain.SmbmsProvider;

import java.util.List;

/**
 * 供应商 Service 接口
 */
public interface ProviderService {

    // 查询供应商列表
    List<SmbmsProvider> getProviderList(String proContact);

    // 添加供应商
    boolean add(SmbmsProvider provider);

    // 根据 ID 查询供应商
    SmbmsProvider getProviderById(Integer id);

    // 修改供应商
    boolean modify(SmbmsProvider provider);

    // 删除供应商
    boolean deleteProviderById(Integer id);
}
