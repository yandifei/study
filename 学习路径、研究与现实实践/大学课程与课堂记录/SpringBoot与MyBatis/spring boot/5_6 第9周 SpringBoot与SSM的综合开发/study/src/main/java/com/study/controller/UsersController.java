package com.study.controller;

import com.study.entity.Users;
import com.study.service.UsersService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 用户控制器
 */
@Controller
@RequestMapping("/users")
public class UsersController {
    
    @Autowired
    private UsersService usersService;
    
    /**
     * 查询所有用户
     */
    @GetMapping("/list")
    public String list(Model model) {
        List<Users> users = usersService.findAll();
        model.addAttribute("users", users);
        return "users/list";
    }
    
    /**
     * 跳转到添加页面
     */
    @GetMapping("/toAdd")
    public String toAdd() {
        return "users/add";
    }
    
    /**
     * 添加用户
     */
    @PostMapping("/add")
    public String add(Users users) {
        usersService.insert(users);
        return "redirect:/users/list";
    }
    
    /**
     * 跳转到编辑页面
     */
    @GetMapping("/toEdit/{uid}")
    public String toEdit(@PathVariable Integer uid, Model model) {
        Users users = usersService.findById(uid);
        model.addAttribute("users", users);
        return "users/edit";
    }
    
    /**
     * 更新用户
     */
    @PostMapping("/update")
    public String update(Users users) {
        usersService.update(users);
        return "redirect:/users/list";
    }
    
    /**
     * 删除用户
     */
    @GetMapping("/delete/{uid}")
    public String delete(@PathVariable Integer uid) {
        usersService.delete(uid);
        return "redirect:/users/list";
    }
}
