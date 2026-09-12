<template>
  <h2 ref="title2">北京</h2>
  <button @click="showLog">点我输出h2</button>
  <Person ref="ren" />
</template>
<!-- 
<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'App',
  components: {
  }
})
</script> -->

<script lang="ts" setup>
import Person from './components/Person.vue';

// 开始干活展示
import { ref } from 'vue'
let title2 = ref()

function showLog() {
  console.log(title2.value)
}
</script>
