import {createRouter, createWebHistory}  from 'vue-router'

import Home from '../components/Home.vue'

const routes = [
    { path: '/', name:'Home', component: Home },
    { path: '/addItem', name:'AddItem', component: ()=>import('../components/AddItemForm.vue') },
    { path: '/item/:id', name:'item.show', component: ()=>import('../components/Item.vue') },
    { path: '/profile', name:'profile.show', component: ()=>import('../components/Profile.vue') },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    linkActiveClass: 'item-active-link'
})

export default router

