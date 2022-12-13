<template>
    Profile
    {{this.user}}
    <!-- {{this.user.city}} -->

    <!-- <div v-for="detail in user">
        {{detail}}
    </div> -->
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
        // console.log(data.username);
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