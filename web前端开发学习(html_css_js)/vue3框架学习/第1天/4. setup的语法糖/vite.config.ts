import { fileURLToPath, URL } from 'node:url'
// Vue 3.3+ 内置了 defineOptions，不需要额外插件
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
// 3.3版本之前的插件调用(它让你能直接在 <script setup> 标签上通过 name 属性给组件命名（省去为了命名而额外写一个普通 <script> 标签的麻烦）)
// import VueSetupExtend from 'vite-plugin-vue-setup-extend'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    // 3.3版本之前的插件调用(它让你能直接在 <script setup> 标签上通过 name 属性给组件命名（省去为了命名而额外写一个普通 <script> 标签的麻烦）)
    // VueSetupExtend(), //现在直接被defineOptions取代了
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
