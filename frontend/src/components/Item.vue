
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
        <div v-if="item.user != this.user.id">
        <input type="number" v-model="amount" />
        <button :disabled="expired_or_not" @click="addBid" type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSeriesModal" style="margin: 1rem">
        Add bid
        </button>
        <input id="question" class="form-control" type="text" required>
        <button type="button" class="btn btn-primary" @click="addQuestion">Add</button>
        </div>

        <h3>Questions and Answers</h3>
        <div v-for="question in this.item.questions">
            <!-- <div v-if=""></div> -->
            {{question.question}} asked by {{ question.posted_by }}
        </div>

    </div>
</template>

<script>

export default {
    name: 'Item',
    props: ['user'],
    data() {
        return {
            item: null,
            users: null,
            expired_or_not: true,
            highest_bidder: null,
            current_price: 0,
            amount: 103,
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

        let res = await fetch("http://localhost:8000/api/getPendingQuestions/"+this.item.id)
        let data = await res.json();
        console.log("this is the reponse");
        console.log(data.questions[0][1].question + " |");
        this.item.questions = data.questions[0];

        // for(let i=0; i<this.item.questions.length; i++) {
        //     console.log(
        //         this.item.questions[i].question + "|" +
        //         this.item.questions[i].posted_by + "|"
        //     );
        // }


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
        async addQuestion() {

            const question = document.getElementById( "question" ).value;
            const response = await fetch('http://localhost:8000/api/addQuestion/', {
                method: 'POST',
                body: JSON.stringify({
                    "user_id": this.user.id,
                    "question": question,
                    "item_id": this.item.id
                })
            });

            let res = await response.json();
            this.item = res;
        }
    }
}


</script>


<style>

</style>
