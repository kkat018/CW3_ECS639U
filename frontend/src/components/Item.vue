
<template>
    <div class="container page-container">

        <!-- <div class="card"> -->
            <!-- {{this.item}} -->
        <!-- <h1>Item: {{this.item.name}}</h1> -->
        <!-- {{item}}
        {{item.description}}
        {{item.starting_price}}
        {{item.date_posted}} -->
        <!-- owner is {{item.owner}} -->
        <div class="container vw-50" style="background-color: lightgrey;">
            <div class="row">
            <div class="col-6" style="border-style: inset;"> Item name: </div>
            <div class="col-6" style="border-style: inset;"> {{item.name}} </div>
            <div class="col-6" style="border-style: inset;"> Desciption: </div>
            <div class="col-6" style="border-style: inset;"> {{item.description}} </div>
            <div class="col-6" style="border-style: inset;"> Starting price: </div>
            <div class="col-6" style="border-style: inset;"> {{item.starting_price}} </div>
            <div class="col-6" style="border-style: inset;"> Date posted: </div>
            <div class="col-6" style="border-style: inset;"> {{item.date_posted}} </div>
            <div class="col-6" style="border-style: inset;"> Expirty date: </div>
            <div class="col-6" style="border-style: inset;"> {{item.expiry_date}} </div>
            <div class="col-6" style="border-style: inset;"> Current price: </div>
            <div class="col-6" style="border-style: inset;"> {{current_price}} </div>
            <div class="col-6" style="border-style: inset;"> Item owner: </div>
            <div class="col-6" style="border-style: inset;"> {{item.owner}} </div>
            </div>
        </div>
        <!-- Button trigger page -->
        <!-- <p>{{this.user}}</p> -->
        <!-- {{this.item}} -->
        <div v-if="this.item.user != this.user.id">
            <input type="number" v-model="amount" />
            <button :disabled="expired_or_not" @click="addBid" type="button" class="inline btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSeriesModal" style="margin: 1rem">
            Add bid
            </button>
        </div>

        <h3 class="mb-16">Ask a Question</h3>
        <div class="flex mb-32">
            <input id="question" class="form-control w-50 inline mr-32" type="text" required>
            <button type="button" class="btn btn-primary" @click="addQuestion">Submit Question</button>
        </div>

        <h3 class="mb-16">Questions and Answers</h3>
        <div class="seperator mb-32" v-for="question in this.item.questions">
            <div v-for="u in this.users">
                <div v-if="u.id == question.posted_by" class="text-left">
                    {{ u.username }} asked...
                </div>
            </div>
            <div class="question">{{question.question}}</div>
            <div v-if="question.answer.length == 0" class="mb-32 text-left">Not answered yet</div>
            <div v-if="question.answer.length > 0" class="mb-32 text-left">ANSWER: {{question.answer}}</div>
            <!-- questionid:{{question.id}}
            user is {{this.user.id}}
            item owner is{{this.item.user}} -->
            <div v-if="this.user.id == this.item.user && question.answer.length == 0" class="flex mb-32">
                <input :id=question.id class="form-control w-50 inline mr-32" type="text" required>
                <button type="button" class="btn btn-primary" @click="addAnswer(question.id)">Submit Answer</button>
            </div>
        </div>

    </div>
</template>

<script>

export default {
    name: 'Item',
    props: ['user'],
    data() {
        return {
            item: {
                id: null,
                name: null,
                date_posted: new Date(),
                starting_price: 0,
                description: "",
                image: "",
                user: null,
                expiry_date: new Date(),
                questions: []
            },
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
            let data = await response.json();
            this.item = data.item;
            console.log(this.item);
            this.expired_or_not = this.item.expiry_date ? new Date(this.item.expiry_date) < Date.now() : true;
        } else {
            console.log("Failed to get item");
        }

        let res = await fetch("http://localhost:8000/api/getPendingQuestions/"+this.item.id)
        let data_q = await res.json();
        this.item.questions = data_q.questions[0];
        console.log(this.item.questions)
        // console.log("this is the reponse");
        // console.log(data.questions[0][1].question + " |");

        // for(let i=0; i<this.item.questions.length; i++) {
        //     console.log(
        //         this.item.questions[i].question + "|" +
        //         this.item.questions[i].posted_by + "|"
        //     );
        // }

        let response_users = await fetch("http://localhost:8000/api/getUsers/")
        const data_users = await response_users.json();
        this.users = data_users.users;
        console.log("users");
        console.log(this.users);
        // console.log(data_users.users[0].id);

        // let res_super = await fetch("http://localhost:8000/api/checkSuperuser/"+this.user.id)
        // const superuser_result = await res_super.json();
        // this.user.superuser =  superuser_result.superuser;
        // console.log(this.user.superuser);
        
        //Email
        // let response_email = await fetch("http://localhost:8000/api/sendEmail/")
        // if (response_email.ok) {
        //     let data = await response.json()
        //     this.item = data.item
        //     this.expired_or_not = this.item.expiry_date ? new Date(this.item.expiry_date) < Date.now() : true
        // } else {
        //     console.log("Failed to get item")
        // }

    },
    methods: {
        async addBid() {
            let response = await fetch("http://localhost:8000/api/item/makeBid", {
                method: "PUT",
                body: JSON.stringify({
                    item_id: this.item.id,
                    user_id: this.user.id,
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

            this.item.questions.push(res);

        },
        async addAnswer(question_id) {
            const answer = document.getElementById( question_id ).value;
            const response = await fetch('http://localhost:8000/api/addAnswer/', {
                method: 'POST',
                body: JSON.stringify({
                    "answer": answer,
                    "question_id": question_id
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
