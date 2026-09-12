<template>
    <div class="person">
        <h1>中国</h1>
        <!-- 在vue中控件的定位用的是ref属性，这样可以防止别的vue文件中出现重复的属性影响定位 -->
        <!-- <h2 id="title2">北京</h2> -->
        <h2 ref="title2">北京</h2>
        <h3>尚硅谷</h3>
        <button @click="showLog">点我输出h2这个元素</button>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// id定位控件
// function showLog() {
//     console.log(document.getElementById('title2'))
// }

//创建一个title2，用于存储ref标记的内容
let title2 = ref()
let a = ref(0)
let b = ref(1)
let c = ref(2)

// ref定位控件
function showLog() {
    console.log(title2.value)
}

/*以前的vue3版本需要
import { defineExpose } from 'vue'
现在我这里都直接变成宏了
*/


// 暴露属性(作为组件的时候是无法被直接访问的，需要通过暴露属性的方式给主页面访问)
defineExpose({ a, b, c })
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