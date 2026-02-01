<template>
    <div class="person">
        <h2>姓名：{{ person.name }}</h2>
        <h2>年龄：{{ person.age }}</h2>
        <h2>汽车：{{ person.car.c1 }}、{{ person.car.c2 }}</h2>
        <button @click="changeName">修改姓名</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="changeC1">修改第一台车</button>
        <button @click="changeC2">修改第二台车</button>
        <button @click="changeCar">修改整个车</button>
    </div>
</template>

<script lang="ts" setup>
import { reactive, watch } from 'vue';

// 数据
let person = reactive({
    name: '张三',
    age: 18,
    car: {
        c1: '奔驰',
        c2: '宝马'
    }
})

// 方法
function changeName() {
    person.name += '~'
}
function changeAge() {
    person.age++
}
function changeC1() {
    person.car.c1 = '奥迪'
}
function changeC2() {
    person.car.c2 = '大众'
}
function changeCar() {
    person.car = {
        c1: '雅迪', c2: '爱玛'
    }
}


// 监听
// // 这个是全体监听，只要person中的任何一个值发生变化，都会触发
// watch(person, (newValue, oldValue) => {
//     console.log("person变化了", newValue, oldValue)
// })

// 仅仅监听person中的name属性
/*错误写法，这个返回的仅仅是一个值，
但是他要的是ref、reactive、一个响应式对象或者结合成的数组
watch(person.name, (newValue, oldValue) => { 

}
*/
// 监视，情况四：监视响应式对象中的某个属性，且该属性时基本类型的，要写成函数式
// watch(() => { return person.name }, (newValue, oldValue) => {
//     console.log("person变化了", newValue, oldValue)
// })


// 监视，情况四：监视响应式对象中的某个属性，且该属性是对象类型的，可以直接写，也能写函数，更推荐写函数
watch(() => person.car, (newValue, oldValue) => {
    console.log("person变化了", newValue, oldValue)
}, { deep: true })

// //监视，情况五：监视上述的多个数据
// watch([() => person.name, person.car], (newvalue, oldvalue) => {
//     console.log('person.car变化了', newvalue, oldvalue)
// }, { deep: true })

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