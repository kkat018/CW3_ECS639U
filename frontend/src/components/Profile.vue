<template>
    <div class="profile">
        <h1 class="mb-32">{{this.user.username}}</h1>
        <div class="flex">
            <figure class="profile__image">
                <img src="../assets/yabe.png" alt={{this.user.username}} width="500" height="600"> 
            </figure>
            <div class="profile__details">
                <div class="mb-32" v-if="this.user.date_of_birth !== null">
                    <p class="heading">Date of Birth</p>
                    <p class="details">{{ this.user.date_of_birth }}</p>
                </div>
                <div v-if="this.user.city !== null">
                    <p class="heading">City</p>
                    <p class="details">{{ this.user.city }}</p>
                </div>
            </div>
        </div>
        {{this.user}}
    </div>
</template>

<script>

export default {
    data() {
        return {
            viewable: false,
            // user: {
            //     id: null,
            //     username: 'Bob',
            //     date_of_birth: new Date(),
            //     city: "",
            //     image: "",
            // },
            user: null,
        }
    },
    async mounted() {
        //Check if user is authenticated [replace with user prop from App.vue]
        let response = await fetch( "http://localhost:8000/api/checkSession", {
            credentials: "include",
            mode: "cors",
            referrerPolicy: "no-referrer"
        } );
        let data = await response.json();
        // JSON.parse(data);
        console.log(data.city);
        if(data.status !==401) {
            this.viewable = true;
            this.user = data;
        }

        //Perform an Ajax request to fetch the user's Profile details
        // let response2 = await fetch( "http://127.0.0.1:8000/api/profile/");
        // let data2 = await response2.json();
        // this.profile = data2.employees;
        // console.log(this.profile);
    }
}

</script>