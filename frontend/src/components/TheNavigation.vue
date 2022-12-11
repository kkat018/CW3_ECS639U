<template>
    <div id="nav">
        <router-link to="/">Home</router-link>
        <router-link to="/item/:id">Item</router-link>
        <router-link to="/Brazil">Brazil</router-link>
        <p>Auction App</p>
    </div>
</template>

<style lang="css">
    #nav .item-active-link {
        color: green;
        border-bottom: 2px soild green;
    }

</style>