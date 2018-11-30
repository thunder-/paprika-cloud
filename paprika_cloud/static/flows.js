//Nodes drop + drag
var currentline = [];
var diagram = [];

var flow = {
    init: function( settings ) {
        flow.config = {
            node_drag: $(".tools .draggable"),
            canvas: $(".canvas")
        };

    flow.dragNode();
    flow.dropNode();
    flow.renderDiagram();
    },

    dragNode: function() {
        var node_drag = flow.config.node_drag;
        node_drag.draggable({
            helper: "clone",
            containment: "document"
        });
    },

    dropNode: function() {
        var canvas = flow.config.canvas;

        canvas.droppable({
            accept: '.tools .draggable',
            drop: function(event, ui) {
                var node = {
                    _id: (new Date).getTime(),
                    position: ui.helper.position()
                };
                node.position.left -= canvas.position().left;
                if (ui.draggable.attr("data-type")) {
                    node.type = ui.draggable.attr("data-type");
                    node.icon = ui.draggable.attr("data-icon");
                    console.log(node.type);
                } else {
                    return;
                }
                diagram.push(node);
                flow.renderDiagram(diagram);
            }
        });
    },

    renderDiagram: function(diagram) {
        var canvas = flow.config.canvas;

        canvas.empty();
        canvas.prepend('<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" id="canvaslines" viewBox="0 0 ' + $('#canvas').width() + ' ' + $('#canvas').height() + '" x="0px" y="0px" xml:space="preserve"></svg>');
        console.log(diagram);
        for(var d in diagram) {
            node = diagram[d];
            var html = '';
            console.log(node.type , node.icon);
            if(node.type && node.icon){
               html = '<div data-type="' + node.type + '" class="card draggable text-center" style="border-bottom: 1px solid rgba(0,0,0,.125);"><div class="card-body card-body-padding pb-1"><a id="'+ node._id +'" href="#" class="text-dark no-decoration valueData">' + node.type + '</a><i class="' + node.icon + ' float-left pr-2 pt-1"></i></div></div>';
            } else {
                return;
            }

            var dom = $(html).css({
                "position": "absolute",
                "top": node.position.top,
                "left": node.position.left
            }).draggable({
                cancel: ".connector",
                drag: function() {
                    updatelines(this);
                },
                containment: "#canvas",
                stop: function(event, ui) {
                    console.log(ui);
                    var id = ui.helper.attr("id");
                    for(var i in diagram) {
                        if(diagram[i]._id == id){
                            diagram[i].position.top = ui.position.top;
                            diagram[i].position.left = ui.position.left;
                        }
                    }
                    stopdrawing();
                    console.log('stop drag');
                },
                grid: [10,10]
            }).attr("id", node._id);
             // Get canvas
            canvas.append(dom);
            addconnectors();
        };
    }
};

$( document ).ready( flow.init );



