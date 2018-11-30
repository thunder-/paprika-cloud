var flow_element = {
    init: function( settings ) {
    },

    createSymbol: function(parent) {
        var symbol = document.createElement("symbol");
        parent.appendChild(symbol);
        return symbol;
    },

    createG: function(parent, id) {
        var g = document.createElement("g");
        g.setAttribute("id", id);
        parent.appendChild(g);
        return g;
    },

    createIn: function(parent) {

        var circle = document.createElement("circle");
        circle.setAttribute("id","in");
        circle.setAttribute("cx","0");
        circle.setAttribute("cy","20");
        circle.setAttribute("r","10");
        circle.setAttribute("fill","gray");
        circle.setAttribute("onclick","flow_ext.connect(evt)");
        parent.appendChild(circle);
        return circle;
    },

    createOut: function(parent, name) {
        width = 40 + parseInt(name.length) * 8 + 25;
        var circle = document.createElement("circle");
        circle.setAttribute("id","out");
        circle.setAttribute("cx",width);
        circle.setAttribute("cy","20");
        circle.setAttribute("r","10");
        circle.setAttribute("fill","gray");
        circle.setAttribute("onclick","flow_ext.connect(evt)");
        parent.appendChild(circle);
        return circle;
    },

    createBox: function(parent, name) {
        var rect = document.createElement("rect");
        console.log("createBox.name", name);
        console.log("createBox.length", name.length);
        width = 40 + parseInt(name.length) * 8 + 25;
        console.log("createBox.width", width);
        rect.setAttribute("class", "draggable");
        rect.setAttribute("width", width);
        rect.setAttribute("height","40");
        rect.setAttribute("fill","white");
        rect.setAttribute("stroke","gray");
        parent.appendChild(rect);
        return rect;
    },

    createBoxLabel: function(parent) {
        var rect = document.createElement("rect");
        rect.setAttribute("class", "draggable");
        rect.setAttribute("width","40");
        rect.setAttribute("height","40");
        rect.setAttribute("fill","gray");
        rect.setAttribute("stroke","gray");
        parent.appendChild(rect);
        return rect;
    },

    createLabel: function(parent, label) {
        var text = document.createElement("text");
        text.setAttribute("class","fas");
        text.setAttribute("x","12");
        text.setAttribute("y","25");
        text.setAttribute("fill","white");
        text.setAttribute("font-size","14");
        text.setAttribute("font-family","FontAwesome");
        text.innerHTML=label;
        parent.appendChild(text);
        return text;
    },

    createName: function(parent, name) {
        var text = document.createElement("text");
        text.setAttribute("x","50");
        text.setAttribute("y","25");
        text.setAttribute("fill","gray");
        text.setAttribute("font-size","16");
        text.setAttribute("font-family","Arial");
        text.innerHTML=name;
        console.log("createName",text);
        parent.appendChild(text);
        return text;

    },

    //        <use x="50" y="300" xlink:href="#node" onmouseup="flow_ext.up(evt)" onmousedown="flow_ext.down(evt)"/>
    createUse: function(parent, id, x, y) {
        var use = document.createElement("use");
        use.setAttribute("x", x);
        use.setAttribute("y", y);
        use.setAttribute("xlink:href","#" + id);
        use.setAttribute("onmouseup","flow_ext.up(evt)");
        use.setAttribute("onmousedown","flow_ext.down(evt)");
        use.setAttribute("onclick","flow_ext.clickNode(evt)");
        parent.appendChild(use);
        return use;
    },

    createStart: function(svg, id, name, label, x, y) {
        var symbol = flow_element.createSymbol(svg);
        var g = flow_element.createG(symbol, id);
        flow_element.createOut(g, name);
        flow_element.createBox(g, name);
        flow_element.createBoxLabel(g);
        flow_element.createLabel(g, label);
        flow_element.createName(g, name);
        flow_element.createUse(svg, id, x, y)
    },

    createEnd: function(svg, id, name, label, x, y) {
        var symbol = flow_element.createSymbol(svg);
        var g = flow_element.createG(symbol, id);
        flow_element.createIn(g);
        flow_element.createBox(g, name);
        flow_element.createBoxLabel(g);
        flow_element.createLabel(g, label);
        flow_element.createName(g, name);
        flow_element.createUse(svg, id, x, y)
    },

    createAction: function(svg, id, name, label, x, y) {
        var symbol = flow_element.createSymbol(svg);
        var g = flow_element.createG(symbol, id);
        flow_element.createIn(g);
        flow_element.createOut(g, name);
        flow_element.createBox(g, name);
        flow_element.createBoxLabel(g);
        flow_element.createLabel(g, label);
        flow_element.createName(g, name);
        flow_element.createUse(svg, id, x, y)
    },

    createPath: function(svg, id, x1, y1, x2, y2) {
        //<path d="M110,119 C222,264 314,115 424,231" />
        var path = document.createElement("path");
        var definition = "M" + x1 + "," + y1 + " C" + (x1+50) +","+ (y1) + " " + (x2-50) + "," + (y2) + " " + x2 + "," + y2;
        path.setAttribute("d", definition);
        path.setAttribute("fill", "transparent");
        path.setAttribute("stroke", "gray");
        path.setAttribute("stroke-width", "2");
        path.setAttribute("id", id);
        path.setAttribute("onclick","flow_ext.clickNode(evt)");
        svg.appendChild(path);
    },

    // label becomes icon, suits better
    createNode: function(svg, node) {
        if (node.type=='start') {
            flow_element.createStart(svg, node.id, node.name, node.label, node.x, node.y);
        } else if (node.type == 'end') {
            flow_element.createEnd(svg, node.id, node.name, node.label, node.x, node.y);
        } else {
            flow_element.createAction(svg, node.id, node.name, node.label, node.x, node.y);
        }
    },

    createDiv: function(parent) {
        var div = document.createElement("div");
        parent.appendChild(div);
        return div;
    },

    createInput: function(parent) {
        var input = document.createElement("input");
        parent.appendChild(input);
        return input;
    },

    createProperty: function(parent, nodeId, name, placeholder, value, disabled=false) {
        var formGroup = flow_element.createDiv(parent);
        formGroup.setAttribute("class", "form-group");

        var formControl = flow_element.createInput(formGroup);
        formControl.setAttribute("class","form-control");
        formControl.setAttribute("name", name);
        formControl.setAttribute("placeholder", name);
        formControl.setAttribute("title", name);
        formControl.setAttribute("value", value);
        formControl.setAttribute("node-id", nodeId);
        formControl.setAttribute("oninput", "flow_ext.input(event)");
        console.log("createProperty.disabled", disabled);

        if (disabled) {
            formControl.setAttribute("disabled", "");
        }
        return formGroup;

    },

    createLoading: function(parent, label) {
        var text = document.createElement("text");
        text.setAttribute("class","fas");
        text.setAttribute("x","350");
        text.setAttribute("y","350");
        text.setAttribute("fill","black");
        text.setAttribute("font-size","60");
        text.setAttribute("font-family","FontAwesome");
        text.innerHTML=label;
        parent.appendChild(text);
        return text;
    },

};




