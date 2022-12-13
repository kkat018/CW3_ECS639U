<template>
    <div class="profile">
        <div class="flex">
            <h1 class="mb-32 mr-32" v-if="this.editMode == false">{{this.user.username}}</h1>
            <p class="mr-32" v-if="this.editMode == true">
                <input id="editUsername" type="text" :value="this.user.username"/>
            </p>
            <div class="flex-column">
                <button v-if="this.editMode == false" @click="toggleEdit()" type="button" class="btn btn-success mt-8">Edit</button>
                <button v-if="this.editMode == true" @click=" editUser()" type="button" class="btn btn-success">Save</button>
            </div>
        </div>
        <div class="flex mt-8">
            <figure class="profile__image" v-if="this.editMode == false">
                <img src="../assets/yabe.png" alt="${this.user.username}" width="500" height="600">
                <!-- <img :src="'../assets/' + user.username"> -->
            </figure>
            <figure class="profile__image" v-if="this.editMode == true">
                 <input type="file" name="fileToUpload" id="fileToUpload">
            </figure>
            <div class="flex-column">
                <div class="flex mb-32" v-if="this.user.date_of_birth !== null">
                    <div class="flex-column mr-32">
                        <p class="heading">Date of Birth</p>
                        <p class="details" v-if="this.editMode == false">
                            {{ this.user.date_of_birth }}
                        </p>
                        <p v-if="this.editMode == true">
                            <input id="editBirthDate" type="date" :value="this.user.date_of_birth"/>
                        </p>
                    </div>
                </div>
                <div class="flex" v-if="this.user.city !== null">
                    <div class="flex-column mr-32">
                        <p class="heading">City</p>
                        <p class="details" v-if="this.editMode == false">
                            {{ this.user.city }}
                        </p>
                        <p v-if="this.editMode == true">
                            <input id="editCity" type="text" :value="this.user.city"/>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {{this.user}}
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
            editMode: false,
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
    },
    methods: {
        async toggleEdit() {
            this.editMode = true;
        },
        async editUser() {
            this.editMode = false;
            let response = await fetch( "http://127.0.0.1:8000/api/profile/", {
                method: "PUT",
                body: JSON.stringify({
                    "id": this.user.id,
                    "username": document.getElementById( "editUsername" ).value,
                    "date_of_birth": document.getElementById( "editBirthDate" ).value,
                    "city": document.getElementById( "editCity" ).value,
                })
            });
            let res = await response.json();

            this.user.username = res.username;
            this.user.date_of_birth = res.date_of_birth;
            this.user.city = res.city;
        },
    }
}

</script>