<template>
    <div class="profile">
        <h1 class="mb-32 mr-32" v-if="this.editMode == false">{{this.user.username}}</h1>
        <p class="mr-32" v-if="this.editMode == true">
            <input id="editUsername" type="text" :value="this.user.username"/>
        </p>
        <div class="flex mt-8">
            <div class="flex mr-32">
                <figure class="profile__image">
                    <img v-if="this.editModeImage == false && this.user.image !== null" :src="'http://localhost:8000' + this.user.image"  :alt="this.user.username" width="500" height="600">
                    <img v-if="this.editModeImage == false && this.user.image == null" :src="'http://localhost:8000/media/default.jpg'" :alt="this.user.username" width="500" height="600">
                    <input v-if="this.editModeImage == true" type="file" class="form-control-file" id="editImage">
                </figure>
                <div class="flex-column">
                    <button v-if="this.editModeImage == false" @click="toggleEditImage()" type="button" class="btn btn-success mt-8">Edit</button>
                    <button v-if="this.editModeImage == true" @click=" editUserImage()" type="button" class="btn btn-success">Save Image</button>
                </div>
            </div>
            <div class="flex">
                <div class="flex-column">
                    <div class="flex mb-32">
                        <div class="flex-column mr-32">
                            <p class="heading">Email</p>
                            <p class="details" v-if="this.editMode == false">
                                {{ this.user.email }}
                            </p>
                            <p v-if="this.editMode == true">
                                <input id="editEmail" type="email" :value="this.user.email"/>
                            </p>
                        </div>
                    </div>
                    <div class="flex mb-32">
                        <div class="flex-column mr-32">
                            <p class="heading">Date of Birth</p>
                            <p class="details" v-if="this.editMode == false">
                                {{ this.user.date_of_birth }}
                            </p>
                            <p v-if="this.editMode == true">
                                <input id="editBirthDate" type="date" :value="this.user.date_of_birth == null ? new Date() : this.user.date_of_birth"/>
                            </p>
                        </div>
                    </div>
                    <div class="flex">
                        <div class="flex-column mr-32">
                            <p class="heading">City</p>
                            <p class="details" v-if="this.editMode == false">
                                {{ this.user.city }}
                            </p>
                            <p v-if="this.editMode == true">
                                <input id="editCity" type="text" :value="this.user.city == null ? 'London' : this.user.city"/>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="flex-column">
                    <button v-if="this.editMode == false" @click="toggleEdit()" type="button" class="btn btn-success mt-8">Edit</button>
                    <button v-if="this.editMode == true" @click=" editUser()" type="button" class="btn btn-success">Save</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    data() {
        return {
            editMode: false,
            editModeImage: false,
        }
    },
    props: ['user'],
    methods: {
        async toggleEdit() {
            this.editMode = true;
        },
        async toggleEditImage() {
            this.editModeImage = true;
        },
        async editUser() {
            this.editMode = false;
            let response = await fetch( "http://127.0.0.1:8000/api/profile/", {
                method: "PUT",
                body: JSON.stringify({
                    "id": this.user.id,
                    "username": document.getElementById( "editUsername" ).value,
                    "email": document.getElementById( "editEmail" ).value,
                    "date_of_birth": document.getElementById( "editBirthDate" ).value,
                    "city": document.getElementById( "editCity" ).value,
                })
            });
            let res = await response.json();
            this.user.username = res.username;
            this.user.email = res.email;
            this.user.date_of_birth = res.date_of_birth;
            this.user.city = res.city;

            console.log(res);
        },
        async editUserImage() {
            this.editModeImage = false;
            const userData = new FormData();
            userData.append('user_id', this.user.id); //need id to know whose image to save into
            userData.append('image', document.getElementById('editImage').files[0]);

            // send the form data object to the server for editing user image
            const response_image = await fetch('http://localhost:8000/api/profile/', {
                method: 'POST',
                body: userData
            });

            // get the response from the server
            if(response_image.ok) {
                alert("Image added successfully");
            } else {
                alert("Image not added");
            }

            //update data state
            let res = await response_image.json();
            this.user.image = res.image
            console.log(res);
        }
    }
}

</script>