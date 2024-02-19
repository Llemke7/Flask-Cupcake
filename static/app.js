$(document).ready(function() {
    // Function to retrive from API and display
    function getCupcakes() {
        axios.get('/api/cupcakes')
            .then(function(response) {
                $('#cupcake-list').empty();
                response.data.cupcakes.forEach(function(cupcake) {
                    $('#cupcake-list').append(`<li>${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}</li>`);
                });
            })
            .catch(function(error) {
                console.error('Error fetching cupcakes:', error);
            });
    }

    // Function to add a new cupcake
    $('#cupcake-form').submit(function(event) {
        event.preventDefault();

        var flavor = $('#flavor').val();
        var size = $('#size').val();
        var rating = $('#rating').val();
        var image = $('#image').val();

        var data = {
            flavor: flavor,
            size: size,
            rating: parseFloat(rating),
            image: image
        };

        axios.post('/api/cupcakes', data)
            .then(function(response) {
                getCupcakes(); 
                $('#cupcake-form')[0].reset(); 
            })
            .catch(function(error) {
                console.error('Error adding cupcake:', error);
            });
    });

    getCupcakes();
});
