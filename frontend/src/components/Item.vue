
<template>
    <div>
        
        <!-- <div class="card"> -->
        <h1>Item: {{item.name}}</h1>
        {{item}}
        {{item.description}}
        {{item.starting_price}}
        {{item.date_posted}}
        owner is {{item.owner}}
        current price is : {{current_price}}
        
        <!-- <div class="card-deck">
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
        </div> -->

        <!-- Button trigger page -->
        <input type="number" v-model="amount" /> 
        <button :disabled="expired_or_not" @click="addBid" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSeriesModal" style="margin: 1rem">
        Add bid
        </button>

        
    </div>
</template>

<script>
// import { ref } from 'vue'

// defineProps({
//   msg: String
// })
export default {
    name: 'Item',
    data() {
        return {
            expired_or_not: true,
            highest_bidder: null,
            current_price: 0,
            amount: 103,
            item: {
                id: null,
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
        let response = await fetch(`http://localhost:8000/api/item/${this.$route.params.id}/`)
        if (response.ok) {
            let data = await response.json()
            this.item = data.item
            this.expired_or_not = this.item.expiry_date ? new Date(this.item.expiry_date) < Date.now() : true
        } else {
            console.log("Failed to get item")
        }
        
    },
    methods: {
        async addBid() {
            let response = await fetch( "http://localhost:8000/api/checkSession", {
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer"
            } );
            let data = await response.json();
            console.log("user id" + data.user_id);
            console.log(this.item.id)
            console.log(this.amount)
            if(data.status !== 401) {            
                let response = await fetch("http://localhost:8000/api/item/makeBid", {
                    method: "PUT",
                    body: JSON.stringify({
                        item_id: this.item.id,
                        user_id: data.user_id,
                        amount: this.amount,
                    })
                });
                if (response.ok) {
                    console.log("yeayy")
                    let data = await response.json()
                    if ('message' in data) {
                        alert(data.message)
                    } else {
                        this.current_price = data.amount
                    }
                    
                    // console.log(this.current_price)
                    // this.highest_bidder = data.user.username
                    
                }
                else {
                    console.log("waaaaaa")
                }
            } else {
                alert("failed to make bid")
            }
        },
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
