
<template>
    <h1>All Items</h1>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addSeriesModal" style="margin: 1rem">Add item</button>
    <div class="destinations">
        <router-link v-for="destination in destinations"
        :key="destination.id"
        :to="{name:'item.show', params:{id:destination.id}}">
            <img :src="`/images/${destination.image}`" alt="destination.name">
        </router-link>
    </div>
</template>

<script>

import sourceData from '../data.json'


export default {
    data() {
        return {
            destinations: sourceData.destinations
        }
    },
}


</script>
