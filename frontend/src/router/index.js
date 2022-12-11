import {createRouter, createWebHistory}  from 'vue-router'

import Home from '../views/Home.vue'
import Item from '../views/Item.vue'

const routes = [
    { path: '/', name:'Home', component: Home },
    { path: '/item/:id', name:'Item', component: Item },
]

const router = createRouter({
    history:createWebHistory(),
    routes
})

export default router

