$(document).ready(function () {
    //API
    var route = ['/api/users', '/api/actions'];
    var globalData = {}

        $.each(route, function(i,u){
            $.ajax(u,{
                type: 'GET',
                dataType: 'json',
                data: '',
                success: function(data) {
                    dataFunction(data);
                }
            })
        });

    function dataFunction(data) {
        globalData = data;
        console.log(globalData);
    }

});


