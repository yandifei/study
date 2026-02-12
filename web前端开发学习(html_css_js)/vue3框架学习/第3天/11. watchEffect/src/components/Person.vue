<template>
    <div class="person">
        <!-- <h2>当前求和为；{{ sum }}</h2>
        <button @click="changeSum">点我sum+1</button> -->
        <h2>需求：当水温达到60度，或水位达到80cm时，给服务器发请求</h2>
        <h2>当前水温：{{ temperature }}℃</h2>
        <h2>当前水位：{{ height }}cm</h2>
        <button @click="changeTemperature">水温+10</button>
        <button @click="changeHeight">水位+10</button>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, watchEffect } from 'vue';

// let sum = ref(0)
// function changeSum() {
//     sum.value++
// }

let temperature = ref(0)
let height = ref(0)

function changeTemperature() {
    temperature.value += 10
}
function changeHeight() {
    height.value += 10
}

/*watchEffect 在依赖多且频繁变化时可能会有轻微性能开销
watch 对于明确知道依赖的场景更精确
实际差异通常不大，代码可读性和维护性更重要
结论：对于你的这个场景（温度或高度达到阈值时发请求），推荐使用 watchEffect
因为它更简洁、直观，且自动追踪依赖的特性减少了维护成本。*/

// 监视
// watch([temperature, height], (newValue, oldValue) => {
//     let [newTemperature, newHeight] = newValue
//     if (newTemperature >= 60 || newHeight >= 80) {
//         console.log('给服务器发请求');
//     }
// })

// 如果数据多就用watchEffect
watchEffect(() => {
    if (temperature.value >= 60 || height.value >= 80) {
        console.log('给服务器发请求');
    }
}


)
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