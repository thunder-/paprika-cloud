//Nodes drop + drag
var currentline = [];
var diagram = [];

var flow_ext = {
    init: function( settings ) {
        console.log("flow_ext.init");
        flow_ext.config = {
            canvas: document.getElementById("canvas"),
            moved: false,
            target: null,
            select: {target: null},
            mode: "select",
            nodes: [],
            connections: [],
            connect: {connection: null, connectionType: null}
        };
        hashcode = localStorage.getItem("hashcode");
        flow_ext.load(hashcode);

    },

    load: function(hashcode) {
        console.log("load", hashcode);
//        var canvas = flow_ext.config.canvas;
//        var svg = canvas.getElementsByTagName('svg')[0];
//        flow_element.createLoading(svg,"&#xf110")
        rest.get_flow(hashcode);
    },

    save: function() {
        console.log("save");
        hashcode = localStorage.getItem("hashcode");
        var nodes = flow_ext.config.nodes;
        console.log("save", nodes);
        rest.save_flow(hashcode, nodes);

        const toast = swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
        });

        toast({
            type: 'success',
            title: 'Saved successfully'
        })

        // setTimeout(
        //     function() {
        //         location.reload();
        //     },700);

    },

    on_save: function(flow) {
        console.log("on_save", flow);
    },

    reset: function() {
        console.log("reset");
        hashcode = localStorage.getItem("hashcode");
        var nodes = flow_ext.config.nodes;
        console.log("reset", nodes);
        rest.reset_flow(hashcode, nodes);

        const swalWithBootstrapButtons = swal.mixin({
            confirmButtonClass: 'btn btn-success',
            cancelButtonClass: 'btn btn-danger',
            buttonsStyling: false,
        })

        swalWithBootstrapButtons({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'No, cancel!',
            reverseButtons: true
        }).then((result) => {
            if (result.value) {
            swalWithBootstrapButtons(
                'Deleted!',
                'Your file has been deleted.',
                'success'
            )
          }
        })

        $(".swal2-confirm.btn.btn-success").click(function() {
             setTimeout(
            function() {
                location.reload();
            },700);
        });




    },

    on_reset: function(flow) {
        console.log("on_reset", flow);
    },

    find_start: function() {
        var nodes = flow_ext.config.nodes;
        for (var i in nodes) {
            node = nodes[i]
            if (node.type=='start') {
                return node;
            }
        }
    },

    find_node_by_id: function(id) {
        var nodes = flow_ext.config.nodes;
        for (var i in nodes) {
            node = nodes[i]
            if (node.id==id) {
                return node;
            }
        }
    },

    find_element_by_id: function(element, id) {
        childs = element.childNodes;
        for (var i in childs) {
            child = childs[i];
            if (child.getAttribute("id")==id) {
                return child;
            }
        }
    },

    find_node_index: function(id) {
        var nodes = flow_ext.config.nodes;
        for (var i in nodes) {
            node = nodes[i];
            if (node.id==id) {
                return i;
            }
        }
    },

    find_connection_index: function(id) {
        var connections = flow_ext.config.connections;
        for (var i in connections) {
            connection = connections[i];
            if (connection.id==id) {
                return i;
            }
        }
    },

    find_connection_by_id: function(id) {
        var connections = flow_ext.config.connections;
        for (var i in connections) {
            connection = connections[i]
            if (connection.id==id) {
                return connection;
            }
        }
    },

    find_connection_by_out: function(id) {
        var connections = flow_ext.config.connections;
        for (var i in connections) {
            connection = connections[i]
            if (connection.out.id==id) {
                return connection;
            }
        }
    },

    find_connection_by_in: function(id) {
        var connections = flow_ext.config.connections;
        for (var i in connections) {
            connection = connections[i]
            if (connection.in.id==id) {
                return connection;
            }
        }
    },


    resolveTarget: function(target) {
        if (target) {
            if (!target.id) {
                target = target.parentElement;
            }
        }
        return target;
    },

    on_load: function(flow) {

        /*var payload_nodes = {"nodes": [ {"id":"1000", "name":"start", "type":"start", "label":"&#xf111;", "x":"300", "y":"250", "out":"1001"}, {"id":"1002", "name":"end", "type":"end", "label":"&#xf111;", "x":"700", "y":"300", "in":"1001"} ]}*/
        /*console.log("payload_nodes", payload_nodes);*/

        if (flow.payload) {
            var payload = JSON.parse(flow.payload);
            console.log("on_load", payload.nodes);

            var canvas = flow_ext.config.canvas;
            var svg = canvas.getElementsByTagName('svg')[0];
            var nodes = flow_ext.config.nodes;


            // load nodes
            for (var i in payload.nodes) {
                var node = payload.nodes[i];
                console.log("on_load.node", node);
                nodes.push(node);
            }

            // load connections
            current = flow_ext.find_start();
            console.log("on_load.current", current);
            console.log(current);
            out = current.out;
            console.log("on_load.out",out);

            while (out) {
                next = flow_ext.find_node_by_id(out);
                connection = { "id": flow_ext.guid(), "out" : {"id": current.id, "x": current.x, "y": current.y}, "in": {"id": next.id, "x": next.x, "y": next.y}}
                flow_ext.config.connections.push(connection);
                //flow_element.createPath(svg,  current.x, current.y, next.x, next.y);

                out = next.out;
                current = next;
            }

            flow_ext.drawNodes(svg);
            flow_ext.drawConnections(svg);

        }
        // redraw
        $("#canvas").html($("#canvas").html());

    },

    drawNodes: function(svg) {
        nodes = flow_ext.config.nodes;
        for (var i in nodes) {
            var node = nodes[i];
            console.log("drawNodes.node", node);
            flow_element.createNode(svg, node);
        }

    },

    drawConnection: function(svg, connection){

        var id = connection.id;

        var out_element = document.getElementById(connection.out.id);
        var out_ = flow_ext.find_element_by_id(out_element,"out");
        console.log("drawConnections.out_", out_);
        var out_cx = out_.getAttribute("cx");
        var out_cy = out_.getAttribute("cy");

        var in_element = document.getElementById(connection.in.id);
        var in_ = flow_ext.find_element_by_id(in_element,"in");
        console.log("drawConnections.in_", in_);
        var in_cx = in_.getAttribute("cx");
        var in_cy = in_.getAttribute("cy");
        flow_element.createPath(svg, id, parseInt(connection.out.x) + parseInt(out_cx), parseInt(connection.out.y)+ parseInt(out_cy), parseInt(connection.in.x)+ parseInt(in_cx), parseInt(connection.in.y)+ parseInt(in_cy));
    },

    drawConnections: function(svg) {
        var connections = flow_ext.config.connections;
        console.log("drawConnections.connections", connections);
        for (var i in connections) {
            var connection = connections[i];
            flow_ext.drawConnection(svg, connection);
        }

    },

    add: function(event) {
        console.log("add", event);


        // retrieve the target, the target could by a div or i.
        // use the id of the div.
        var target = event.target;
        if (!target.id) {
            target = event.target.parentElement;
        }

        console.log("add.target.id", target.id);
        var properties = target.getAttribute("data-properties");
        if (properties) {
            properties = JSON.parse(properties);
        }

        console.log("add.target.properties", properties.length)
        var canvas = flow_ext.config.canvas;
        var svg = canvas.getElementsByTagName('svg')[0];
        var guid = flow_ext.guid();
        var nodes = flow_ext.config.nodes;

        console.log("add.target.data-icon-unicode", target.getAttribute("data-icon-unicode"));
        var label = target.getAttribute("data-icon-unicode");
        if (!label) {
            label = "&#xf111;";
        }
        var node = {"type": target.id, "id": flow_ext.guid(), "name": target.id, "label": label, "x":"300", "y": "300", "properties": properties};

        nodes.push(node);

        const toast = swal.mixin({
          toast: true,
          position: 'top',
          showConfirmButton: false,
          timer: 1400
        });

        toast({
          type: 'success',
          title: ' '+ node.name +' has been added'
        })

        // svg, type, id, name, label, x, y
        flow_element.createNode(svg, node);

        // redraw
        $("#canvas").html($("#canvas").html());

    },

    down: function(event) {
        event.preventDefault();
        console.log("down", event);
        flow_ext.config.target = event.target;
        flow_ext.config.mode = "move";
        var x = event.clientX;
        var y = event.clientY;
        flow_ext.config.x = x;
        flow_ext.config.y = y;
    },

    up: function(event) {
        console.log("up", event);
        flow_ext.config.mode="select";
        flow_ext.config.target = null;
    },

    clickNode: function(event) {
        event.stopPropagation();
        var moved = flow_ext.config.moved;
        console.log("clickNode.moved", moved);

        if (moved==false) {
            // set the focus to the canvas, for key events;
            canvas = flow_ext.config.canvas;
            canvas.focus();
            console.log("clickNode.event", event);
            flow_ext.abort(event);
            flow_ext.config.mode="select";

            var target = flow_ext.config.select.target;
            if (target === event.target) {

                tagName = event.target.tagName;
                if (tagName=="use") {
                    // deselect the node (use)
                    var id = event.target.getAttribute("xlink:href").replace("#","");

                    // find the g element.
                    var g = document.getElementById(id);
                    var rect = g.getElementsByTagName('rect')[0]
                    rect.setAttribute("stroke","gray");
                    rect.setAttribute("stroke-width", "1");

                    var rect = g.getElementsByTagName('rect')[1]
                    rect.setAttribute("stroke","gray");
                    rect.setAttribute("stroke-width", "1");
                    rect.setAttribute("fill", "gray");
                    console.log("nodeClick.unselect.select.rect", rect);
                    console.log("nodeClick.unselect.target", event.target);
                } else {
                    // deselect the connection (path)
                    event.target.setAttribute("stroke", "gray");
                    event.target.setAttribute("stroke-width", "2");
                }

                flow_ext.config.select.target = null;
            } else {
                if (target) {
                    var tagName = target.tagName;

                    if (tagName=="use") {
                        // deselect the other node (use)
                        var id = target.getAttribute("xlink:href").replace("#","");

                        // find the g element.
                        var g = document.getElementById(id);
                        var rect = g.getElementsByTagName('rect')[0]
                        rect.setAttribute("stroke","gray");
                        rect.setAttribute("stroke-width", "1");

                        var rect = g.getElementsByTagName('rect')[1]
                        rect.setAttribute("stroke","gray");
                        rect.setAttribute("stroke-width", "1");
                        rect.setAttribute("fill", "gray");
                    } else {
                        // deselect the other connection (path)
                        target.setAttribute("stroke", "gray");
                        target.setAttribute("stroke-width", "2");
                    }
                }

                console.log("nodeClick.select.target", event.target);

                var tagName = event.target.tagName;

                if (tagName=="use") {
                     // resolve the id from the target (the use element)
                    var id = event.target.getAttribute("xlink:href").replace("#","");

                    // find the g element.
                    var g = document.getElementById(id);

                    var rect = g.getElementsByTagName('rect')[0]
                    rect.setAttribute("stroke","#8ab2dc");
                    rect.setAttribute("stroke-width", "4");
                    var rect = g.getElementsByTagName('rect')[1]
                    rect.setAttribute("stroke","#8ab2dc");
                    rect.setAttribute("fill","#8ab2dc");
                    rect.setAttribute("stroke-width", "4");
                    console.log("nodeClick.select.rect", rect);


//                    var circle = g.getElementsByTagName('rect')[0]
//                    circle.setAttribute("fill","#fff");
//                    var circle = g.getElementsByTagName('circle')[1]
//                    circle.setAttribute("fill","#fff");

                    var node = flow_ext.find_node_by_id(id);
                    console.log("nodeClick.node", node);
                    flow_ext.showProperties(node);

                } else {
                    event.target.setAttribute("stroke", "#8ab2dc");
                    event.target.setAttribute("stroke-width", "3");
                }
                flow_ext.config.select.target = event.target;
            }

        }
        flow_ext.config.moved=false;


    },

    input: function(event) {
        console.log('input', event);
        var nodeId = event.target.getAttribute("node-id");
        var inputName = event.target.name;
        var node = flow_ext.find_node_by_id(nodeId);

        if (inputName == "name") {
            node.name = event.target.value;
            var canvas = flow_ext.config.canvas;
            var svg = canvas.getElementsByTagName('svg')[0];
            var nodeElement = document.getElementById(node.id);
            var textElement = nodeElement.getElementsByTagName("text")[1];
            textElement.innerHTML = event.target.value;
        } else {
            var properties = node.properties;
            for (var i in properties) {
                var property = properties[i];

                for (var j in property) {
                    var name = j;
                    if (name == inputName) {
                        var value = event.target.value;
                        property[j] = value;
                    }
                }
            }
        }
    },

    showProperties: function(node) {
        console.log("showProperties", node);
        var groupElement = document.getElementById("properties");

        // remove existing properties.
        while (groupElement.firstChild) {
            groupElement.removeChild(groupElement.firstChild);
        }

        // add the fixed properties
        // id, name, placeholder, value
        flow_element.createProperty(groupElement, node.id, "type", "Type", node.type, true);
        flow_element.createProperty(groupElement, node.id, "name", "Name", node.name);


        // add the properties
        var properties = node.properties;
        for (var i in properties) {
            var property = properties[i];
            for (var j in property) {
                var name = j;
                var value = property[j];
                if (value) {

                    var type = typeof property[j];
                    if (type == "object") {
                        value = JSON.stringify(property[j]);

                    }
                }
                if (groupElement) {
                    flow_element.createProperty(groupElement, node.id, name, name, value);
                }
            }
        }

    },

    keyUp: function(event) {
        console.log("keyup.event", event);
        if (event.keyCode == 46) {
            flow_ext.delete();
        }
    },

    delete: function() {

        canvas = flow_ext.config.canvas;

        mode = flow_ext.config.mode;
        if (mode=="select") {
            target = flow_ext.config.select.target;

            tagName = target.tagName;
            if (tagName=="use") {
                 // resolve the id from the target (the use element)
                var id = target.getAttribute("xlink:href").replace("#","");

                out_ = flow_ext.find_connection_by_out(id);
                if (out_) {
                    out_element = document.getElementById(out_.id);

                    console.log("delete.connections", flow_ext.config.connections );
                    index = flow_ext.find_connection_index(out_.id);
                    flow_ext.config.connections.splice(index, 1);
                    console.log("delete.connections", flow_ext.config.connections );
                    console.log("delete.connection",connection);
                    out_element.remove();
                }

                in_ = flow_ext.find_connection_by_in(id);
                if (in_) {
                    in_element = document.getElementById(in_.id);

                    console.log("delete.connections", flow_ext.config.connections );
                    index = flow_ext.find_connection_index(in_.id);
                    flow_ext.config.connections.splice(index, 1);
                    console.log("delete.connections", flow_ext.config.connections );
                    console.log("delete.connection",connection);
                    in_element.remove();
                }

                index = flow_ext.find_node_index(id);
                flow_ext.config.nodes.splice(index,1);
                console.log("nodes.nodes", flow_ext.config.nodes );
                target.remove();
            } else {
                connection = flow_ext.find_connection_by_id(target.id);

                node = flow_ext.find_node_by_id(connection.out.id);
                node.out = "";
                console.log("delete.node", node);

                node = flow_ext.find_node_by_id(connection.in.id);
                node.in = "";
                console.log("delete.node", node);


                index = flow_ext.find_connection_index(target.id);
                flow_ext.config.connections.splice(index, 1);
                target.remove();

                console.log("delete.nodes", flow_ext.config.nodes);
            }
        }
    },

    move: function(event) {
        mode = flow_ext.config.mode;
        if (mode=="move") {
            if (flow_ext.config.hasOwnProperty('target')) {
                var target = flow_ext.config.target;
                if (target) {

                    // resolve the id from the target (the use element)
                    var id = target.getAttribute("xlink:href").replace("#","");

                    // find the node from nodes.
                    var node = flow_ext.find_node_by_id(id);

                    var dx = event.clientX - flow_ext.config.x;
                    var dy = event.clientY - flow_ext.config.y;

                    target.setAttribute("x", parseInt(node.x) + parseInt(dx));
                    target.setAttribute("y", parseInt(node.y) + parseInt(dy));
                    flow_ext.config.x = event.clientX;
                    flow_ext.config.y = event.clientY;



                    // move the node
                    node.x = parseInt(node.x) + parseInt(dx);
                    node.y = parseInt(node.y) + parseInt(dy);

                    // move the out connection
                    var connection = flow_ext.find_connection_by_out(id);
                    if (connection) {
                        connection.out.x = parseInt(connection.out.x) + parseInt(dx);
                        connection.out.y = parseInt(connection.out.y) + parseInt(dy);

                        var path = document.getElementById(connection.id);
                        var d = path.getAttribute("d").split(" ");
                        var c = d[0].split(",");
                        var x = c[0].replace("M","");
                        var y = c[1];
                        var x = parseInt(x) + parseInt(dx);
                        var y = parseInt(y) + parseInt(dy);
                        d[0] = "M"+ x + "," + y;

                        var c = d[1].split(",");
                        var x = c[0].replace("C","");
                        var y = c[1];
                        var x = parseInt(x) + parseInt(dx);
                        var y = parseInt(y) + parseInt(dy);
                        d[1] = "C"+ x + "," + y;

                        path.setAttribute("d",d.join(" "));
                    }
                    // move the in connection
                    var connection = flow_ext.find_connection_by_in(id);
                    if (connection) {
                        connection.in.x = parseInt(connection.in.x) + parseInt(dx);
                        connection.in.y = parseInt(connection.in.y) + parseInt(dy);

                        path = document.getElementById(connection.id);
                        var d = path.getAttribute("d").split(" ");
                        var c = d[3].split(",");
                        var x = c[0]
                        var y = c[1];
                        x = parseInt(x) + parseInt(dx);
                        y = parseInt(y) + parseInt(dy);
                        d[3] = x + "," + y;

                        c = d[2].split(",");
                        x = c[0];
                        y = c[1];
                        x = parseInt(x) + parseInt(dx);
                        y = parseInt(y) + parseInt(dy);
                        d[2] = x + "," + y;

                        path.setAttribute("d",d.join(" "));
                        //console.log("node.path", d);
                    }
                    flow_ext.config.moved = true;
                }
            }
        }
//        } else if (mode=="connect") {
//            var connection = flow_ext.config.connect.connection;
//            var dx = event.clientX - flow_ext.config.connect.x;
//            var dy = event.clientY - flow_ext.config.connect.y;
//            flow_ext.config.connect.x = event.clientX;
//            flow_ext.config.connect.y = event.clientY;
//
//            console.log("move.connect.connection", connection);
//            path = document.getElementById(connection.id);
//            console.log("move.path", path);
//            var d = path.getAttribute("d").split(" ");
//            var c = d[3].split(",");
//            var x = c[0]
//            var y = c[1];
//            x = parseInt(x) + parseInt(dx);
//            y = parseInt(y) + parseInt(dy);
//            d[3] = x + "," + y;
//
//            c = d[2].split(",");
//            x = c[0];
//            y = c[1];
//            x = parseInt(x) + parseInt(dx);
//            y = parseInt(y) + parseInt(dy);
//            d[2] = x + "," + y;
//
//            path.setAttribute("d",d.join(" "));
//        }
    },

    abort: function(event) {
        mode = flow_ext.config.mode;
        console.log("abort", event);
        if (mode == "connect") {

//            var connection = flow_ext.config.connect.connection;
//            if (connection) {
//                path = document.getElementById(connection.id);
//                path.remove();
//            }

            flow_ext.config.mode = "select";
            flow_ext.config.connect.connection = null;
            flow_ext.config.connect.connectionType = null;
        } else if (mode == "select") {
        }
    },

    hasConnection: function(connectionType, id) {
        // check if there is already a connection
        var connection = null;
        if (connectionType=="out") {
            connection = flow_ext.find_connection_by_out(id);
        }

        if (connectionType=="in") {
            connection = flow_ext.find_connection_by_in(id);
        }

        if (connection) {
            return true;
        }
        return false;
    },

    connect: function(event) {
        console.log("connect", event);

        // ensure this is the last event raised.
        event.stopPropagation();

        if (!flow_ext.config.connect.connection) {
            console.log("connect.start");
            flow_ext.config.mode = "connect";

            var connectionType = event.target.id;
            console.log("connect.connectionType", connectionType);

            var nodeElement = event.target.parentElement;
            console.log("connect.nodeElement", nodeElement);

            // only start drawing if there is no connection
            console.log("connect.hasConnection", !flow_ext.hasConnection(connectionType, nodeElement.id));
            if (flow_ext.hasConnection(nodeElement.id)) {
                console.log("connect.hasConnection", flow_ext.hasConnection(connectionType, nodeElement.id));
                return;
            }

            var out_ = flow_ext.find_element_by_id(nodeElement, connectionType);
            var node = flow_ext.find_node_by_id(nodeElement.id);
            console.log("connect.out_", out_);
            console.log("connect.node", node);

            var x = parseInt(node.x) ;
            var y = parseInt(node.y) ;

            var connection = null;
            if (connectionType=="out") {
                connection = {"id": flow_ext.guid(), "in": {"id": "", "x": x, "y": y}, "out": {"id": node.id, "x": x, "y": y}};
            } else {
                connection = {"id": flow_ext.guid(), "in": {"id": node.id, "x": x, "y": y}, "out": {"id": "", "x": x, "y": y}};
            }
            flow_ext.config.connect.connection = connection;
            flow_ext.config.connect.connectionType = connectionType;

//            // for detecting relative mouse movement
//            var wx = event.clientX;
//            var wy = event.clientY;
//            flow_ext.config.connect.x = wx;
//            flow_ext.config.connect.y = wy;
//
//            var canvas = flow_ext.config.canvas;
//            var svg = canvas.getElementsByTagName('svg')[0];
//
//            var cx = out_.getAttribute("cx");
//            var cy = out_.getAttribute("cy");
//            flow_element.createPath(svg, connection.id, x + parseInt(cx), y+parseInt(cy), x + parseInt(cx), y+ parseInt(cy));
//            //flow_ext.drawConnection(svg, connection);
//
//            // redraw
//            $("#canvas").html($("#canvas").html());

            console.log("connect.connection", connection);

        } else {
            console.log("connect.end");
            var connectionType = event.target.id;
            var connection = flow_ext.config.connect.connection;
            console.log("connect.connection", connection);
            // connectionTypes of start and end must differ.
            var startConnectionType = flow_ext.config.connect.connectionType;
            if (startConnectionType==connectionType) {
                console.log("connect.connectiontype.equals", startConnectionType, connectionType);
                return;
            }

            var nodeElement = event.target.parentElement;
            console.log("connect.nodeElement", nodeElement);

            // only start drawing if there is no connection
            if (flow_ext.hasConnection(nodeElement.id)) {
                console.log("connect.hasConnection", flow_ext.hasConnection(nodeElement.id));
                return;
            }

            var endNode = flow_ext.find_node_by_id(nodeElement.id);

            var startNode = null;
            if (connectionType=="in") {
                startNode = flow_ext.find_node_by_id(connection.out.id);
            } else {
                startNode = flow_ext.find_node_by_id(connection.in.id);
            }

            console.log("connect.endNode", endNode);
            console.log("connect.startNode", startNode);

            var x = parseInt(endNode.x) ;
            var y = parseInt(endNode.y) ;
            console.log("connect.x", x);
            console.log("connect.y", y);

            // set the in part of the connection
            if (connectionType=="in") {
                connection.in.id = endNode.id;
                connection.in.x = x;
                connection.in.y = y;
            } else {
                connection.out.id = endNode.id;
                connection.out.x = x;
                connection.out.y = y;
            }

            // set the in and out of the nodes;
            if (connectionType=="in") {
                startNode.out = endNode.id;
                endNode.in = startNode.id;
            } else {
                startNode.in = endNode.id;
                endNode.out = startNode.id;
            }
            console.log("connect.connection", connection);
            // console.log("connect.nodes", nodes);


            var connections = flow_ext.config.connections;
            connections.push(connection);

            var canvas = flow_ext.config.canvas;
            var svg = canvas.getElementsByTagName('svg')[0];

            flow_ext.drawConnection(svg, connection);

            // redraw
            $("#canvas").html($("#canvas").html());

            flow_ext.config.connect.connection = null;
            flow_ext.config.connect.connectionType = null;
        }

    },

    guid: function() {
//        return Math.floor((1 + Math.random()) * 0x10000).toString(32);
        return Math.random().toString().substring(3);
    }
};

$( document ).ready( flow_ext.init );



