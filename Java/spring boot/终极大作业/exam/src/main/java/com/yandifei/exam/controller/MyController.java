package com.yandifei.exam.controller;

import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.yandifei.exam.domain.*;
import com.yandifei.exam.service.*;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;

/**
 * 超市订单管理系统 Controller
 */
@Controller
public class MyController {

    @Autowired
    private UserService userService;

    @Autowired
    private RoleService roleService;

    @Autowired
    private ProviderService providerService;

    @Autowired
    private BillService billService;

    // ==================== 登录相关 ====================

    @GetMapping({"/", "/login"})
    public String login() {
        return "login";
    }

    @PostMapping("/dologin")
    public String doLogin(@RequestParam String userCode,
                          @RequestParam String userPassword,
                          HttpSession session,
                          Model model) {
        Users user = userService.login(userCode, userPassword);
        if (user != null) {
            session.setAttribute("user", user);
            return "redirect:/welcome";
        } else {
            model.addAttribute("error", "用户名或密码错误！");
            return "login";
        }
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.removeAttribute("user");
        return "redirect:/login";
    }

    @GetMapping("/welcome")
    public String welcome(HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        return "welcome";
    }

    // ==================== 用户管理 ====================

    @RequestMapping(value = "/userlist", method = {RequestMethod.GET, RequestMethod.POST})
    public String userList(@RequestParam(defaultValue = "1") Integer pageNum,
                           @RequestParam(required = false) String queryname,
                           @RequestParam(required = false, defaultValue = "0") Integer queryUserRole,
                           HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        List<SmbmsRole> roleList = roleService.getRoleList();
        model.addAttribute("roleList", roleList);

        PageHelper.startPage(pageNum, 5);
        List<Users> userList = userService.getUserListByPage(queryname, queryUserRole);
        PageInfo<Users> pageInfo = new PageInfo<>(userList);

        model.addAttribute("pageInfo", pageInfo);
        model.addAttribute("queryUserName", queryname);
        model.addAttribute("queryUserRole", queryUserRole);

        return "userlist";
    }

    @GetMapping("/useradd")
    public String userAdd(HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        List<SmbmsRole> roleList = roleService.getRoleList();
        model.addAttribute("roleList", roleList);
        return "useradd";
    }

    @PostMapping("/useraddsave")
    public String userAddSave(Users user,
                              HttpSession session,
                              @RequestParam(required = false)
                              @DateTimeFormat(pattern = "yyyy-MM-dd") Date birthday) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        user.setBirthday(birthday);
        Users loginUser = (Users) session.getAttribute("user");
        user.setCreatedBy(loginUser.getId());
        user.setCreationDate(new Date());

        if (userService.add(user)) {
            return "redirect:/userlist";
        }
        return "useradd";
    }

    @GetMapping("/userview")
    public String userView(@RequestParam Integer uid, HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        Users user = userService.getUserById(uid);
        model.addAttribute("user", user);
        return "userview";
    }

    @GetMapping("/usermodify")
    public String userModify(@RequestParam Integer uid, HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        Users user = userService.getUserById(uid);
        model.addAttribute("user", user);
        List<SmbmsRole> roleList = roleService.getRoleList();
        model.addAttribute("roleList", roleList);
        return "usermodify";
    }

    @PostMapping("/usermodifysave")
    public String userModifySave(Users user,
                                 HttpSession session,
                                 @RequestParam(required = false)
                                 @DateTimeFormat(pattern = "yyyy-MM-dd") Date birthday) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        user.setBirthday(birthday);
        Users loginUser = (Users) session.getAttribute("user");
        user.setModifyBy(loginUser.getId());
        user.setModifyDate(new Date());

        if (userService.modify(user)) {
            return "redirect:/userlist";
        }
        return "usermodify";
    }

    // ===== JSON 接口：检查用户编码是否存在 =====
    @GetMapping("/ucexist")
    @ResponseBody
    public String checkUserCodeExist(@RequestParam String userCode) {
        Users user = userService.getUserByUserCode(userCode);
        if (user != null) {
            return "{\"userCode\":\"exist\"}";
        }
        return "{\"userCode\":\"noexist\"}";
    }

    // ===== JSON 接口：删除用户 =====
    @GetMapping("/deluser")
    @ResponseBody
    public String deleteUser(@RequestParam(required = false) String method,
                             @RequestParam(required = false) Integer uid) {
        if (uid != null && userService.deleteUserById(uid)) {
            return "{\"delResult\":\"true\"}";
        }
        return "{\"delResult\":\"false\"}";
    }

    // ==================== 供应商管理 ====================

    @RequestMapping(value = "/providerlist", method = {RequestMethod.GET, RequestMethod.POST})
    public String providerList(@RequestParam(defaultValue = "1") Integer pageNum,
                               @RequestParam(required = false) String proContact,
                               HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }

        PageHelper.startPage(pageNum, 5);
        List<SmbmsProvider> providerList = providerService.getProviderList(proContact);
        PageInfo<SmbmsProvider> pageInfo = new PageInfo<>(providerList);

        model.addAttribute("pageInfo", pageInfo);
        model.addAttribute("proContact", proContact);

        return "providerlist";
    }

    @GetMapping("/provideradd")
    public String providerAdd(HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        return "provideradd";
    }

    @PostMapping("/provideraddsave")
    public String providerAddSave(SmbmsProvider provider, HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        Users loginUser = (Users) session.getAttribute("user");
        provider.setCreatedBy(loginUser.getId());
        provider.setCreationDate(new Date());

        if (providerService.add(provider)) {
            return "redirect:/providerlist";
        }
        return "provideradd";
    }

    @GetMapping("/providerview")
    public String providerView(@RequestParam Integer providerid, HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        SmbmsProvider provider = providerService.getProviderById(providerid);
        model.addAttribute("provider", provider);
        return "providerview";
    }

    @GetMapping("/providermodify")
    public String providerModify(@RequestParam Integer providerid, HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        SmbmsProvider provider = providerService.getProviderById(providerid);
        model.addAttribute("provider", provider);
        return "providermodify";
    }

    @PostMapping("/providermodifysave")
    public String providerModifySave(SmbmsProvider provider, HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        provider.setModifyDate(new Date());

        if (providerService.modify(provider)) {
            return "redirect:/providerlist";
        }
        return "providermodify";
    }

    // ===== JSON 接口：删除供应商 =====
    @GetMapping("/delprovider")
    @ResponseBody
    public String deleteProvider(@RequestParam(required = false) String method,
                                 @RequestParam(required = false) Integer providerid) {
        if (providerid != null && providerService.deleteProviderById(providerid)) {
            return "{\"delResult\":\"true\"}";
        }
        return "{\"delResult\":\"false\"}";
    }

    // ==================== 订单管理 ====================

    @RequestMapping(value = "/orderslist", method = {RequestMethod.GET, RequestMethod.POST})
    public String ordersList(@RequestParam(defaultValue = "1") Integer pageNum,
                             @RequestParam(required = false) String productName,
                             @RequestParam(required = false) String proContact,
                             HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        // 获取供应商列表用于搜索下拉
        List<SmbmsBill> distinctList = billService.getDistinctBillList();
        model.addAttribute("distinctList", distinctList);

        PageHelper.startPage(pageNum, 5);
        List<SmbmsBill> billList = billService.getBillListByPage(productName, proContact);
        PageInfo<SmbmsBill> pageInfo = new PageInfo<>(billList);

        model.addAttribute("pageInfo", pageInfo);
        model.addAttribute("productName", productName);
        model.addAttribute("proContact", proContact);

        return "orderslist";
    }

    @GetMapping("/ordersadd")
    public String ordersAdd(HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        List<SmbmsBill> distinctList = billService.getDistinctBillList();
        model.addAttribute("distinctList", distinctList);
        return "ordersadd";
    }

    @PostMapping("/ordersaddsave")
    public String ordersAddSave(SmbmsBill bill, HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        Users loginUser = (Users) session.getAttribute("user");
        bill.setCreatedBy(loginUser.getId());
        bill.setCreationDate(new Date());

        if (billService.add(bill)) {
            return "redirect:/orderslist";
        }
        return "ordersadd";
    }

    @GetMapping("/ordersview")
    public String ordersView(@RequestParam Integer billid, HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        SmbmsBill bill = billService.getBillById(billid);
        model.addAttribute("bill", bill);
        return "ordersview";
    }

    @GetMapping("/ordersmodify")
    public String ordersModify(@RequestParam Integer billid, HttpSession session, Model model) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        SmbmsBill bill = billService.getBillById(billid);
        model.addAttribute("bill", bill);
        List<SmbmsBill> distinctList = billService.getDistinctBillList();
        model.addAttribute("distinctList", distinctList);
        return "ordersmodify";
    }

    @PostMapping("/ordersmodifysave")
    public String ordersModifySave(SmbmsBill bill, HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        bill.setModifyDate(new Date());

        if (billService.modify(bill)) {
            return "redirect:/orderslist";
        }
        return "ordersmodify";
    }

    // ===== JSON 接口：删除订单 =====
    @GetMapping("/delbill")
    @ResponseBody
    public String deleteBill(@RequestParam(required = false) String method,
                             @RequestParam(required = false) Integer billid) {
        if (billid != null && billService.deleteBillById(billid)) {
            return "{\"delResult\":\"true\"}";
        }
        return "{\"delResult\":\"false\"}";
    }

    // ==================== 密码修改 ====================

    @GetMapping("/changepassword")
    public String changePassword(HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        return "changepassword";
    }

    // 密码修改 AJAX 验证旧密码
    @GetMapping("/jsp/user.do")
    @ResponseBody
    public String pwdModify(@RequestParam(required = false) String method,
                            @RequestParam(required = false) String oldpassword,
                            HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "{\"result\":\"sessionerror\"}";
        }
        if ("pwdmodify".equals(method)) {
            Users user = (Users) session.getAttribute("user");
            if (oldpassword == null || oldpassword.isEmpty()) {
                return "{\"result\":\"error\"}";
            }
            if (user.getUserPassword().equals(oldpassword)) {
                return "{\"result\":\"true\"}";
            } else {
                return "{\"result\":\"false\"}";
            }
        }
        return "{\"result\":\"false\"}";
    }

    // 密码修改提交
    @PostMapping("/changepasswordsave")
    public String changePasswordSave(@RequestParam String userPassword,
                                     HttpSession session) {
        if (session.getAttribute("user") == null) {
            return "syserror";
        }
        Users user = (Users) session.getAttribute("user");
        user.setUserPassword(userPassword);
        userService.modify(user);
        session.removeAttribute("user");
        return "redirect:/login";
    }

}
