<template>
    <div>
        <!-- <button @click="fetchMovies"> Fetch Movies</button> -->
        <div>
            <ul>
                <li v-for="item in items">
                    {{item.name}}
                </li>
            </ul>
        </div>
        
        <Home title="My favourite TV list" class="vh-100"/>
    </div>
</template>

<script>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import Home from "./components/Home.vue";
// import Modal from "./components/Modal.vue"

export default {
    components: {
        Home,
        
    },
    data() {
        return {
            items: [],
            item: {
                name: null,
                date_posted: new Date()
            }
        }
    },
    methods: {
        async fetchMovies() {
            //perform AJAX request to fetch movies
            let response = await fetch("http://localhost:8000/api/movies/")
            let data = await response.json()
            this.items = data.items
        },
    }
}
</script>

<style scoped>
/* .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
}
.logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
} */
</style>
