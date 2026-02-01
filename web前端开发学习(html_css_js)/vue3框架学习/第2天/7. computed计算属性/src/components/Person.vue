<template>
    <div class="person">
        姓：<input type="text" v-model="firstName">
        <br>
        名：<input type="text" v-model="lastName">
        <br>
        <button @click="changeFullName">将全名改为li-si</button>
        全名：<span>{{ fullName }}</span>
        全名：<span>{{ fullName }}</span>
        全名：<span>{{ fullName }}</span>
        全名：<span>{{ fullName }}</span>
        全名：<span>{{ fullName }}</span>
        全名：<span>{{ fullName }}</span>
        全名：<span>{{ fullName }}</span>
        <!-- 全名：<span>{{ fullName2() }}</span>
        全名：<span>{{ fullName2() }}</span>
        全名：<span>{{ fullName2() }}</span>
        全名：<span>{{ fullName2() }}</span>
        全名：<span>{{ fullName2() }}</span>
        全名：<span>{{ fullName2() }}</span>
        全名：<span>{{ fullName2() }}</span> -->
    </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';

let firstName = ref("雁")
let lastName = ref("低飞")

/*通函数 (function)
这是一个标准 JavaScript 函数。
如果在模板中调用它，每次组件重新渲染时，该函数都会被重新执行，没有缓存。
*/
function fullName2() {
    return firstName.value.slice(0, 1).toUpperCase() + firstName.value.slice(1) + '-' + lastName.value
}

/*计算属性 (computed)
这段代码利用了 Vue 的响应式系统。
computed 会根据它依赖的变量（firstName 和 lastName）的变化自动重新计算，并且具有缓存机制
这么定义的fullName是一个计算属性，且是只读的，这个值不能被直接修改
*/
// let fullName = computed(() => {
//     console.log(1)
//     return firstName.value.slice(0, 1).toUpperCase() + firstName.value.slice(1) + '-' + lastName.value
// })

/*这样的计算属性就可以修改了而不是只读，computed返回的是ref的对象*/
let fullName = computed({
    // 把原来的箭头函数换成get和set函数
    get() {
        return firstName.value.slice(0, 1).toUpperCase() + firstName.value.slice(1) + '-' + lastName.value
    },
    // 必定会传回一个值，这个值就是被修改后的值
    set(val) {
        const [str1, str2] = val.split("-")
        firstName.value = str1
        lastName.value = str2
        // console.log("set", val)

    }
})

function changeFullName() {
    fullName.value = "li-si"
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