<template>
    <div>
        <TheNavigation :user="user"/>
        <div v-if="viewable==true">
            <router-view :user="user"></router-view>
        </div>
        <div class="container" v-if="viewable==false">
            <h2>You are not logged in.</h2>
        </div>
    </div>
</template>

<script>

import TheNavigation from './components/TheNavigation.vue'

export default {
    components: {TheNavigation},
    data() {
        return {
            viewable: false,
            user: null
        }
    },
    async created() {
        //Check if user is authenticated
        let response = await fetch( "http://localhost:8000/api/checkSession", {
            credentials: "include",
            mode: "cors",
            referrerPolicy: "no-referrer"
        } );
        let data = await response.json();
        console.log(data.status);
        if(data.status !==401) {

            this.viewable = true;
            this.user = data;
            console.log("user id ffrom App:");
            console.log(this.user.id);
        }
    }
}



</script>





