<template>
    <div id="nav">
        <div class="nav__inner">
            <div class="flex center">
                <h1 id="main-title">Auction App</h1>
                <router-link to="/">Home</router-link>
                <router-link to="/profile">Profile</router-link>
            </div>
            <div class="center">
                <div class="flex center" v-if="viewable==true">
                    <p class="mb-0 mr-32">Welcome {{this.user}}</p>
                    <a href="http://localhost:8000/logout">Logout</a>
                </div>
                <div class="center" v-if="viewable==false">
                    <a href="http://localhost:8000/login">Login</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {

    data() {
        return {
            viewable: false,
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
        console.log(data.id);
        if(data.status !==401) {
            this.viewable = true;
            this.user = data;
        }
    }
}


</script>



<style lang="css">
    #nav .item-active-link {
        color: green;
        border-bottom: 2px soild green;
    }

</style>

