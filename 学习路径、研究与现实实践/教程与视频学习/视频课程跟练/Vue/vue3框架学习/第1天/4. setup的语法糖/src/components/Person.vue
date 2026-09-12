<template>
    <div class="person">
        <h2>姓名:{{ name }}</h2>
        <h2>年龄:{{ age }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="showTel">查看联系方式</button>
    </div>
</template>

<!-- 不写下面这个的话默认name就是文件命 -->
<!-- <script lang="ts">
    export default {
        name: 'Person',
        
        // setup基础用法（这种写法是基础）：
        // setup(){
        //     // 数据
        //     let name = "张三" //注意此时的name不是响应式的
        //     let age = 18 //注意此时的age不是响应式的
        //     let tel = "1234567890"

        //     // 方法
        //     function showTel(){
        //         alert(tel)
        //     }
        //     function changeName(){
        //         name = "zhang-san"
        //     }
        //     function changeAge(){
        //         age += 1
        //     }

        //     // 返回
        //     return {name, age, tel, showTel, changeName, changeAge}
            
        // }
    }
</script> -->

<!-- .setup的语法糖 -->
<!-- vue3.3版本以上可以用在setup内直接使用defineOptions(){}命名，无需npm i vite-plugin-vue-setup-extend -D插件 -->
<!-- <script lang="ts" setup name="Person234"> -->

<script lang="ts" setup>
// 需要导入包

defineOptions({
    name: 'Person'
})
// 数据
let name = "张三" //注意此时的name不是响应式的
let age = 18 //注意此时的age不是响应式的
let tel = "1234567890"

// 方法
function showTel() {
    alert(tel)
}
function changeName() {
    name = "zhang-san"
}
function changeAge() {
    age += 1
}

// 不用再写返回值了，它默认会返回所有声明的变量和方法
</script>

<style scoped>
/* 样式 */
.person {
    background-color: skyblue;
    box-shadow: 0 0 10px;
    border-radius: 10px;
    padding: 20px;
}

button {
    margin: 0 5px;
}
</style>