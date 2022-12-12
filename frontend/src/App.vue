<template>
    <div>
        <TheNavigation/>
        <div class="container" v-if="viewable==true">
            <router-view></router-view>
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
            viewable: false
        }
    },
    async mounted() {
        //Perform an Ajax request to fetch the list of employees
        let response = await fetch( "http://localhost:8000/api/checkSession", {
            credentials: "include",
            mode: "cors",
            referrerPolicy: "no-referrer"
        } );
        let data = await response.json();
        console.log(data);
        if(data.status !==401) {
            this.viewable = true;
        }
    }
}



</script>





