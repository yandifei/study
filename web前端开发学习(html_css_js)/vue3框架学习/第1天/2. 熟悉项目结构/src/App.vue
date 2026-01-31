<template>
    <!-- html -->
     <div class="app">
        <h1>hello world</h1>
        <Person></Person>
     </div>
</template>

<script lang="ts">
    import Person from './components/Person.vue';
    // JS或TS
    export default {
        name: 'App', // 组件名
        // 注册组件
        components: {
            Person
        }
    }

</script>

<style>
    /* 样式 */
    .app{
        background-color: #ddd;
        box-shadow: 0 0 10px;
        border-radius: 10px;
        padding: 20px;
    }
</style>