
<template>
    <div>
        <h1>All Items</h1>
        <router-link to="/addItem">
            <button @click="addItem" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSeriesModal" style="margin: 1rem">
                Add item
            </button>
        </router-link>

        <div class="input-group mb-3">
            <input v-model="search_input" type="text" class="form-control" placeholder="Search item by name/description" aria-label="Searchbar" aria-describedby="searchButton">
            <button @click="search" class="btn btn-outline-secondary" type="button" id="searchButton">Search</button>
            <button @click="clear" class="btn btn-outline-secondary" type="button" id="clearButton">Clear</button>
        </div>

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
    </div>
</template>

<script>
// import { ref } from 'vue'

// defineProps({
//   msg: String
// })
export default {
    name: 'Home',
    props: ["title"],
    data() {
        return {
            search_input: "",
            items: [],
            item: {
                name: null,
                date_posted: new Date(),
                starting_price: 0,
                description: "",
                image: "",
                user: null,
                expiry_date: new Date(),
            },
        }
    },
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
        async search() {
            let response = await fetch(`http://localhost:8000/api/search/${this.search_input}`)
            if (response.ok) {
                let data = await response.json()
                this.items = data.items
            } else {
                alert("Failed to search items")
            }
        },
        async clear() {
            this.search_input = ""
            let response = await fetch('http://localhost:8000/api/items/')
            if (response.ok) {
                let data = await response.json()
                this.items = data.items
            } else {
                console.log("Failed to get items")
            }
        },
    }
}

</script>
