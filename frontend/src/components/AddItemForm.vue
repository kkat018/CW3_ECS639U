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
            <label for="image">Example file input</label>
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
    data() {
        return {
            
        }
    },
    methods: {
        async listItem(){
            let name = document.getElementById("name");
            let price = document.getElementById("price");
            let description = document.getElementById("description");
            let date = document.getElementById("dateTime");
            let response = await fetch( "http://127.0.0.1:8000/api/addItem/",
                {
                    method: 'POST',
                    body: JSON.stringify({
                        "name": name.value,
                        "price": price.value,
                        "description": description.value,
                        "expiry_date": date.value
                    })
                }
            );
            let data = await response.json();
            console.log(data)
            // this.employees.push( data );
        }
    }
}



</script>