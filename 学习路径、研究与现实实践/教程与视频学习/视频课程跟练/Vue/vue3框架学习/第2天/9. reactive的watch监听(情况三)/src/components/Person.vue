<template>
    <div class="person">
        <h1>情况三：监视【reactive】定义的【对象类型】数据</h1>
        <h2>姓名：{{ person.name }}</h2>
        <h2>年龄：{{ person.age }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="changePerson">修改整个人</button>
    </div>
</template>

<script lang="ts" setup>
import { reactive, watch } from 'vue';
// 数据
// >情况三
let person = reactive({
    name: '张三',
    age: 18,
})

// 方法
// 情况三
function changeName() {
    person.name += '~';
};
function changeAge() {
    person.age++;
};
//监视，情况三：监视【reactive】定义的【对象类型】数据，且默认是开启深度监视的
function changePerson() {
    // 这个语法实际上就是在person中把name,age的属性替换了而不是弄了个新的person，在ref中就是弄了一个新的
    Object.assign(person, { name: '李四', age: 20, })
    console.log(person);
}

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