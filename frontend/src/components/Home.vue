
<template>
    <div class="border rounded bg-warning shadow pt-4 vw-100 vh-100 p-3">
        <h1>{{title}}</h1>
        <!-- <div class="card"> -->
        
        <!-- Button trigger page -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSeriesModal" style="margin: 1rem">
        Add item
        </button>
        {{items}}
        <div class="card-deck">
            <div class="row" >
                <div v-for="item in items" :key="item.id" class="col-sm-4">
                    <div  class="card" style="width: 18rem;">
                        <div class="card-body">
                            <h5 class="card-title">{{item.title}}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">Release date: {{item.date_posted}}</h6>
                            <p class="card-text">TV show <br/> Number of seasons: {{item.expiry_date}} <br/> Has ended: {{item.starting_price}} </p>
                            
                            
                            <button @click="deleteSeries(item)" type="button" class="btn btn-light">Open</button>
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
    props: ["title"],
    data() {
        return {
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
            console.log(data.items)
        } else {
            console.log("Failed to get items")
        }
    },
    methods: {
        // async fetchItems() {
        //     //perform AJAX request to fetch items
        //     let response = await fetch("/api/items/")
        //     let data = await response.json()
        //     this.items = data.items
        // },
        
    }
}


</script>


<style>

</style>
