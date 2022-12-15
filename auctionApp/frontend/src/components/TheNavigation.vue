<template>
    <div id="nav">
        <div class="nav__inner">
            <div class="flex center">
                <p id="main-title">Auction App</p>
                <router-link to="/">Home</router-link>
                <router-link to="/profile">Profile</router-link>
            </div>
            <div class="center">
                <div class="flex center" v-if="this.user !== null">
                    <p class="mb-0 mr-32">Welcome {{this.user.username}}!</p>
                    <a href="http://localhost:8000/logout">Logout</a>
                </div>
                <div class="center" v-if="this.user == null">
                    <a href="http://localhost:8000/login">Login</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    props: ['user']
}


</script>



<style lang="css">
    #nav .item-active-link {
        color: green;
        border-bottom: 2px soild green;
    }

</style>

