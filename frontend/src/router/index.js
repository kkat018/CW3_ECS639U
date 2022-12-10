import {createRouter, createWebHistory}  from 'vue-router'

const routes = [
    {
        path:'/',
        name:"Home",
        component:()=>import('../components/pages/Home.vue')
    },
    {
        path:'/item/:id',
        name:"Item",
        component:()=>import('../components/pages/Item.vue')
    },
]

const router = createRouter({
    history:createWebHistory(),
    routes
})

export default router

// import Vue from "vue";
// import Router from "vue-router";

// import Home from "../components/home/Home.vue";

// Vue.use(Router);

// export default new Router({
//     routes: [
//         {
//         path: "/",
//         name: "Home",
//         component: Home,
//         },
//     ],
// });
