<template>
    <TheNavigation/>
    <div clas="container">
        <router-view></router-view>
    </div>

</template>

<script>

import TheNavigation from './components/TheNavigation.vue'

export default {
    components: {TheNavigation}
}

</script>





