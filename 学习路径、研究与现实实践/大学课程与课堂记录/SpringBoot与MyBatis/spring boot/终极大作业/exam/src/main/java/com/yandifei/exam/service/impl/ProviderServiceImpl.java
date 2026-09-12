package com.yandifei.exam.service.impl;

import com.yandifei.exam.dao.ProviderMapper;
import com.yandifei.exam.domain.SmbmsProvider;
import com.yandifei.exam.service.ProviderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 供应商 Service 实现
 */
@Service
public class ProviderServiceImpl implements ProviderService {

    @Autowired
    private ProviderMapper providerMapper;

    @Override
    public List<SmbmsProvider> getProviderList(String proContact) {
        return providerMapper.show_Provider(proContact);
    }

    @Override
    public boolean add(SmbmsProvider provider) {
        return providerMapper.add(provider) > 0;
    }

    @Override
    public SmbmsProvider getProviderById(Integer id) {
        return providerMapper.getProviderById(id);
    }

    @Override
    public boolean modify(SmbmsProvider provider) {
        return providerMapper.modify(provider) > 0;
    }

    @Override
    public boolean deleteProviderById(Integer id) {
        return providerMapper.deleteProviderById(id) > 0;
    }
}
