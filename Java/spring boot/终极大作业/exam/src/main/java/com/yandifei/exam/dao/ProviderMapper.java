package com.yandifei.exam.dao;

import com.yandifei.exam.domain.SmbmsProvider;
import org.apache.ibatis.annotations.Param;

import java.util.List;

/**
 * 供应商 Mapper 接口
 */
public interface ProviderMapper {

    // 查询供应商列表（带条件搜索）
    List<SmbmsProvider> show_Provider(@Param("proContact") String proContact);

    // 添加供应商
    int add(SmbmsProvider provider);

    // 根据 ID 查询供应商
    SmbmsProvider getProviderById(@Param("id") Integer id);

    // 修改供应商
    int modify(SmbmsProvider provider);

    // 删除供应商
    int deleteProviderById(@Param("id") Integer id);
}
