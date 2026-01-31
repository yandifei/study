<template>
    <div class="person">
        <!-- <h2>姓名:{{ name }}</h2>
        <h2>年龄:{{ age }}</h2>
        <button @click="changeName">修改名字</button>
        <button @click="changeAge">修改年龄</button>
        <button @click="showTel">查看联系方式</button> -->
        <h2>一辆{{ car.brand }}车，价值{{ car.price }}万</h2>
        <button @click="changePrice">修改汽车的价格</button>
        <button @click="changeCar">修改汽车名称</button>
        <h2>游戏列表</h2>
        <ul>
            <li v-for="g in games" :key="g.id">{{ g.name }}</li>
        </ul>
        <button @click="changeFirstGame">修改第一个游戏的名字</button>
        <h2>测试：{{ obj.a.b.c }}</h2>
        <button @click="changeobj">测试</button>
    </div>
</template>

<script lang="ts" setup>
// 响应式数据布局需要导入ref
import { ref, reactive } from 'vue'

defineOptions({
    name: "Person",
})

//数据，原来是写在data中的，此时的name、age、tel都不是响应式的数据
// let name = "张三"
// let age = 18
// let tel = "1234567890"

// 响应式数据
/*需要注意的式ref是支持所有类型(基本数据类型和对象类型)，reactive仅限对象类型
官方推荐ref，但是视频要求区分也就是有错，ref一把梭，reactive会出意想不到的问题
*/
let name = ref("张三")
let age = ref(18)
let tel = "1234567890"
let address = "地址"
// 对象类型
let car = ref({ brand: "奔驰", price: 100 })
// 不推荐的写法
// let car = reactive({ brand: "奔驰", price: 100 })
let games = ref([
    { id: 'aysdytfsatro1', name: '王者荣耀' },
    { id: 'aysdytfsatro2', name: '原神' },
    { id: 'aysdytfsatro3', name: '三国志' }
])

// 深层次的嵌套和绑定
let obj = reactive({
    a: {
        b: {
            c: 666
        }
    }
})

console.log(1, name)
console.log(2, age)
console.log(3, tel)
console.log(4, address)

// 方法
function showTel() {
    alert(tel)
}
function changeName() {
    name.value = "zhang-san"
}
function changeAge() {
    age.value += 1
    // 写法没有报错，但是age本来就是ref了，所有这样写会导致age失去响应式
    age = ref(9)
}

function changePrice() {
    car.value.price += 10
    console.log(car.value)
}

function changeCar() {
    // 对于对象类型reactivate不能这样定义，不然会失去响应
    // car.value = {brand: '奥拓',price:1} // 这么写页面不更新的
    // car.value = reactive({brand:'奥拓',price:1}) // 这么写页面不更新的

    // 在reactivate定义的数据对象中，下面这个写法页面可以更新
    Object.assign(car.value, { brand: "宝马" })
}

function changeFirstGame() {
    games.value[0]!.name = "英雄联盟"
}

function changeobj() {
    obj.a.b.c = 999
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