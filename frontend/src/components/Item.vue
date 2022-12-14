
<template>
    <div>
        <!-- <h1>{{title}}</h1> -->
        <!-- <div class="card"> -->
        
        {{item}}
        
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
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSeriesModal" style="margin: 1rem">
        Add bid
        </button>
        
        <div class="input-group mb-3">
            <input id='question' type="text" class="form-control" placeholder="Ask a question!" aria-label="Question"
                aria-describedby="button-addon2">
            <div class="input-group-append">
                <button class="btn btn-primary" type="button" id="button-addon2" @click="add_question">Submit</button>
            </div>
        </div>

        <button class="btn btn-primary" type="button" @click="get_questions">Get Questions</button>
        <div v-if="show">
            <div v-for="q in question">
                {{q}} 
                <!-- <div>
                    <button class="btn btn-primary" type="button" @click="add_answer">
                        ADD ANSWER
                    </button> <input id='question' type="text" class="form-control" placeholder="Answer!" aria-label="Answer"
                            aria-describedby="button-addon2">
                </div> -->
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
    name: 'Item',
    data() {
        return {
            item: {
                name: null,
                date_posted: new Date(),
                starting_price: 0,
                description: "",
                image: "",
                user: null,
                expiry_date: new Date(),
            },
            question: {
                question: null
            },
            show: false
        }
    },
    async created() {
        let response = await fetch(`http://localhost:8000/api/item/${this.$route.params.id}/`)
        if (response.ok) {
            let data = await response.json()
            this.item = data.item
        } else {
            console.log("Failed to get item")
        }
    },
    methods: {
        // async fetchItems() {
        //     //perform AJAX request to fetch items
        //     let response = await fetch("/api/items/")
        //     let data = await response.json()
        //     this.items = data.items
        // },56`§§

        async add_question() {
            // lines 89 to 96 get current user id
            let response = await fetch("http://localhost:8000/api/checkSession", {
                credentials: "include",
                mode: "cors",
                referrerPolicy: "no-referrer"
            });
            let data = await response.json();
            let user_id = data['user_id']

            let question = document.getElementById('question')
            let response1 = await fetch( "http://127.0.0.1:8000/api/addQuestion/" , 
            {
                method: 'POST',
                body: JSON.stringify({
                    "text": question.value,
                    "user_id": user_id,
                    "item": this.item,
                })
            });
            let data2 = await response1.json();
            this.get_questions();
        },

        async get_questions() {
            this.show=true
            let response = await fetch(`http://127.0.0.1:8000/api/renderQuestions/${this.$route.params.id}`)
            let data = await response.json();
            let question = []
            for (var i=0; i<data.length; i++){
                question[i] = (data[i].fields.text)
            }
            this.question = question
            return {};
        },

        // async add_answer(){
        //     let item_owner = this.item.user.id

        //     let response = await fetch("http://localhost:8000/api/checkSession", {
        //         credentials: "include",
        //         mode: "cors",
        //         referrerPolicy: "no-referrer"
        //     });
        //     let data = await response.json();
        //     console.log("question:", data['user_id']);
        //     let user_id = data['user_id']

        //     if(user_id==item_owner){
        //         console.log("successs")
        //     }

        // }
    }
}


</script>


<style>

</style>
