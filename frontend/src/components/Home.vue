
<template>
    <h1>All Items</h1>
       <router-link to="/addItem">
           <button @click="addItem" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSeriesModal" style="margin: 1rem">
                Add item
            </button>
        </router-link>
    <div class="destinations">
        <router-link v-for="destination in destinations"
        :key="destination.id"
        :to="{name:'destination.show', params:{id:destination.id}}">
            <img :src="`/images/${destination.image}`" alt="destination.name">
        </router-link>
    </div>

    <!-- Nada's code -->
    {{items}}
        <div class="card-deck">
            <div class="row" >
                <div v-for="item in items" :key="item.id" class="col-sm-4">
                    <div  class="card" style="width: 18rem;">
                        <div class="card-body">
                            <h5 class="card-title">{{item.name}}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">Release date: {{item.date_posted}}</h6>
                            <p class="card-text">TV show <br/> Number of seasons: {{item.expiry_date}} <br/> Has ended: {{item.starting_price}} </p>

                            <button @click="goToItem(item)" type="button" class="btn btn-light">Open</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    <!--  -->

</template>

<script>

import sourceData from '../data.json'

// import { ref } from 'vue'

// defineProps({
//   msg: String
// })
export default {
    name: 'Home',
    props: ["title"],
    data() {
        return {
            destinations: sourceData.destinations, //temporary code for printing dummy data
            // items: [],
            // item: {
            //     name: null,
            //     date_posted: new Date(),
            //     starting_price: 0,
            //     description: "",
            //     image: "",
            //     user: null,
            //     expiry_date: new Date(),
            // },
        }
    },
    // Nada's code:
    async created() {
        let response = await fetch('http://localhost:8000/api/items/')
        if (response.ok) {
            let data = await response.json()
            this.items = data.items
        } else {
            console.log("Failed to get items")
        }
    },
    methods: {
        goToItem(item) {
            console.log(item)
            //perform AJAX request to fetch items
            this.$router.push({path: `/item/${item.id}` })
            // let response = await fetch("/api/items/")
            // let data = await response.json()
            // this.items = data.items
        },

    }
}

</script>
