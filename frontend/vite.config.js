import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig(({command, mode}) => {
    return {
      plugins: [vue()],
      build: {
        emptyOutDir: true,
        outDir: '../static/auctionApp/vue',
      },
      base: (mode == 'development') ? 'http://localhost:5173' : '/static/auctionApp/vue/',
      // server: {
      //   port: 8001
      // }
    }
})
