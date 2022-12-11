import {createRouter, createWebHistory}  from 'vue-router'

import Home from '../components/Home.vue'

const routes = [
    { path: '/', name:'Home', component: Home },
    { path: '/Brazil', name:'Brazil', component: ()=>import('../components/Brazil.vue') },
    { path: '/item', name:'Item', component: ()=>import('../components/Item.vue') },
    { path: '/item/:id', name:'destination.show', component: ()=>import('../components/ItemShow.vue') },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    linkActiveClass: 'item-active-link'
})

export default router

