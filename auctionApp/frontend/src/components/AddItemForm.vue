<template>
    <form>
        <div class="form-group form-item">
        <label for="name">Name</label>
        <input id="name" class="form-control" placeholder="Diary of a Wimpy Kid" maxlength="100" required>
        </div>
        <div class="form-group form-item">
            <label for="price">Starting Price (£)</label>
            <input id="price" class="form-control" type="number" placeholder="32" required>
        </div>
        <div class="form-group form-item flex" id="file-input">
            <label for="image">Image</label>
            <input type="file" class="form-control-file" id="image">
        </div>
        <div class="form-group form-item">
            <label for="description">Description</label>
            <textarea class="form-control" id="description" rows="2" maxlength="250" required></textarea>
        </div>
        <div class="form-group form-item">
            <label for="dateTime">Expiry Date</label>
            <input id="dateTime" class="form-control" name="date" type="datetime-local" required>
        </div>
        <button type="button" class="btn btn-primary" @click="listItem">Add</button>
    </form>

</template>

<script>


export default {
    props: ['user'],
    methods: {
        async listItem(){
            // create a new form data object
            const itemData = new FormData();
            // append the name input's value to the form data object
            itemData.append('name', document.getElementById('name').value);
            // append the description input's value to the form data object
            itemData.append('description', document.getElementById('description').value);
            // append the price input's value to the form data object
            itemData.append('price', document.getElementById('price').value);
            // append the image input's value to the form data object
            itemData.append('image', document.getElementById('image').files[0]);
            // append the date input's value to the form data object
            itemData.append('date', document.getElementById('dateTime').value);
            // append the user_id input's value to the form data object
            itemData.append('user_id', this.user.id);

            // send the form data object to the server for uploading itemData
            const response = await fetch('http://localhost:8000/api/addItem/', {
                // MUST USE POST METHOD for uploading images
                method: 'POST',
                body: itemData
            });

            // get the response from the server
            if(response.ok) {
                // if the response is ok, then the item was uploaded successfully
                alert("Item added successfully");
            } else {
                // if the response is not ok, then the item was not uploaded successfully
                alert("Item not added");
            }
        }
    }
}



</script>