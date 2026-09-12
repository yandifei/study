<template>
    <div class="person">
        <h1>情况一：监视【ref】的【基本数据】类型</h1>
        <h2>当前求和为:{{ sum }}</h2>
        <button @click="changeSum">点我sum+1</button>
        <br>
        <h1>情况二：监视【ref】定义的【对象类型】数据</h1>
        <h2>姓名：{{ person.name }}</h2>
        <h2>年龄：{{ person.age }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="changePerson">修改整个人</button>

    </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from 'vue';
// 数据
// 情况一
let sum = ref(0);
// 情况二
let person = ref({
    name: '张三',
    age: 18,
})

// 方法
// 情况一
function changeSum() {
    sum.value++;
};
// 情况二
function changeName() {
    person.value.name += '~';
};
function changeAge() {
    person.value.age++;
};
function changePerson() {
    person.value = { name: '李四', age: 20 };
}

// 监视，情况一：监视【ref】定义的【基本类型】数据
/*在 Vue.js 中，watch 函数返回一个用于停止监听的函数。
这个返回的函数就是用来取消对数据的监听的，从而停止执行回调函数。*/
const stopWatch = watch(sum, (newValue, oldValue) => {
    console.log('sum的值发生了变化', newValue, oldValue);
    if (newValue >= 10) {
        stopWatch(); // 停止监听
    }
})

//监视，情况二：监视【ref】定义的【对象类型】数据，监视的是对象的地址值，若想监视对象内部属性的变化
/*
watch的第一个参数是：被监视的数据
watch的第二个参数是：监视的回调
watch的第三个参数是：配置对象（deep、immediate）
deep: true代表深度监视，监视深度对象数据类型
immediate：相当于do while，会在初始化时先执行一次这个监视函数
*/
watch(person, (newValue, oldvalue) => {
    console.log('person变化了', newValue, oldvalue)
}, { deep: true, immediate: true })

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