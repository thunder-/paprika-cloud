var rest = {
    init: function( settings ) {
        console.log("init");
    },

    get_flow: function(hashcode, nodes) {
        console.log("get_flow", hashcode);
        $.ajax({
            type: 'GET',
            dataType: 'json',
            data: '',
            url: '/rest/get_flow?hashcode='+ hashcode,
            success: function(data) {
                console.log("get_flow.data", data);
                flow_ext.on_load(data);
            }
        });
    },

    save_flow: function(hashcode, nodes) {
        console.log("save_flow", nodes);
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            data: JSON.stringify({hashcode: hashcode, nodes: nodes}),
            url: '/rest/save_flow',
            success: function(data) {
                console.log("save_flow.data", data);
                flow_ext.on_save(data);
            }
        });
    },

    reset_flow: function(hashcode, nodes) {
        console.log("reset_flow", nodes);
        $.ajax({
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            data: JSON.stringify({hashcode: hashcode, nodes:nodes}),
            url: '/rest/reset_flow',
            success: function(data) {
                console.log("reset_flow.data", data);
                flow_ext.on_save(data);
            }
        });
    },


};

$( document ).ready( rest.init );



