<template>
    <div class="person">
        <h2>姓名:{{ name }}</h2>
        <h2>年龄:{{ age }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive, toRefs, toRef } from 'vue'

// 在 Vue 3.5 中，响应式解构功能仅适用于在 <script setup> 中从 defineProps 解构出来的 Props，并非适用于所有 reactive 对象

// 数据
let person = reactive({
    name: '张三',
    age: 18
})

// 注意：下面进行了解构赋值
// toRefs 将 reactive 对象中的每个属性都转换为 ref 对象，这样就可以在模板中使用响应式数据
let { name, age } = toRefs(person)
// toRef 将 reactive 对象中的某个属性转换为 ref 对象，这样就可以在模板中使用响应式数据
let n1 = toRef(person, 'name')
console.log(n1)

// 方法
function changeName() {
    name.value += '~'
    console.log(name, person.name)
}

function changeAge() {
    age.value += 1
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