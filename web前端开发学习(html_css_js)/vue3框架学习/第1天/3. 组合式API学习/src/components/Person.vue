<template>
    <div class="person">
        <h2>姓名:{{name}}</h2>
        <h2>年龄:{{age}}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="showTel">查看联系方式</button>
        <hr>
        <h2>测试1：{{a}}</h2>
        <h2>测试2：{{c}}</h2>
        <button @click="b">测试</button>
    </div>
</template>

<script lang="ts">
    export default {
        name: 'Person',

        // vue2的写法(选项式或配置式)
        // data(){
        //     return {
        //         name: '张三',
        //         age: 18,
        //         tel: '1234567890'
        //     }
        // },
        // 
        // methods: {
        //     showTel(){
        //         alert(this.tel)
        //     },
        //     changeName(){
        //         this.name = "zhang-san"
        //     },
        //     changeAge(){
        //         this.age += 1
        //     }
        // }
        
        /* vu2可以和vue3混用，但是不推荐（埋雷：vue3中setup的生命周期在beforeCreated之前，
        所有setup后他是有this指针可以被vue2访问到的）
        */
        // vue2代码
        data(){
            return {
                a:  'a',
                c: this.name
            }
        },
        methods: {
            b(){
                console.log('b')
            }
        },

        // vue3代码
        setup(){
            // 数据
            let name = "张三" //注意此时的name不是响应式的
            let age = 18 //注意此时的age不是响应式的
            let tel = "1234567890"

            // 方法
            function showTel(){
                alert(tel)
            }
            function changeName(){
                name = "zhang-san"
            }
            function changeAge(){
                age += 1
            }

            // 返回
            return {name, age, tel, showTel, changeName, changeAge}
            
        }
    }
    
</script>

<style scoped>
    /* 样式 */
    .person{
        background-color: skyblue;
        box-shadow: 0 0 10px;
        border-radius: 10px;
        padding: 20px;
    }
    button{
        margin: 0 5px;
    }
</style>