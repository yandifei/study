<template>
  <person />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Person from './components/Person.vue';

export default defineComponent({
  name: 'App',
  components: {
    person: Person
  }
})
</script>
