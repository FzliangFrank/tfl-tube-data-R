

from IPython.display import display, HTML
import json

'''
This first version creates some issue 
when dragged the node and text don't move but eventually not moving at all
'''
__zoom_js_v1 = '''
    // Create object handle zoom event

    // Create a new zoom behavior
    const zoom = d3.zoom()
        .scaleExtent([1/2, 64])
        .on("zoom", zoomed);
    // Append a new element type "rect" as a child elemetn
    const zoomRect = svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all")
    // Now you Apply zoom behavour defined in the first step to the rectabgle
    let transform = d3.zoomIdentity;
    function zoomed(event) {{
        transform = event.transform;
        node.attr("transform", event.transform);
        link.attr("transform", event.transform);
        text1.attr("transform", event.transform);
        text2.attr("transform", event.transform);
    }}
    zoomRect
        .call(zoom)
        .call(zoom.translateTo, 0, 0); // translateTo define scale element
'''
__zoom_js_v2 = '''
    // Create object handle zoom event
    // (zoom: before creating node) Append a new element type "rect" as a child elemetn
    const zoomRect = svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all")
    // Zoom Behavour
    // Create a new zoom behavior
    const zoom = d3.zoom()
        .scaleExtent([1/2, 64])
        .on("zoom", zoomed);
    // Now you Apply zoom behavour defined in the first step to the rectabgle
    let transform = d3.zoomIdentity;
    function zoomed(event, d) {{
        transform = event.transform;
        node.attr("transform", event.transform);
        link.attr("transform", event.transform);
        text1.attr("transform", event.transform);
        text2.attr("transform", event.transform);
        //simulation.attr("transform", event.transform);
    }}
    zoomRect
        .call(zoom)
        //.call(zoom.translateTo, 1, 1); // bug: this element somehow cause edge node mismatch

'''

def vis(json_data, centre_strength = 60):

    html_code_2 = f"""
    <p id="dev"></p>
    <div id="d3-graph"> </div>
    <script type="module">

    import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

    // Parse the Python data passed to the script
    const graphData = {json_data};

    // Set the dimensions of the graph
    const width = 1200;
    const height = 800;
    const node_repel = -50
    const node_color_fill = "#f4d03f"
    const link_color = "#839192"
    
    
    // Append an SVG element to the div with id 'd3-graph'
    const svg = d3.select("#d3-graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .style('max-width', '100%')
        .style('height', 'auto')

    

    // Define the force simulation
    const simulation = d3.forceSimulation(graphData.nodes)
        .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(100))
        .force("charge", d3.forceManyBody().strength(node_repel))
        .force("center", d3.forceCenter(width / 2, height / 2));

    // Create the link (line) elements
    const link = svg.append("g")
        .selectAll("line")
        .data(graphData.links)
        .enter().append("line")
        .attr("stroke", link_color)
        .attr("stroke-width", 2);


    // Create the node (circle) elements
    const node = svg.append("g")
        .selectAll("circle")
        .data(graphData.nodes)
        .enter().append("circle")
        .attr("r", 5)
        .attr("fill", node_color_fill)
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round")
        .call(drag(simulation));

    // Add Label To Node: This technique is adding element instead of text on top of label
    const text1 = svg.append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(graphData.nodes)
        .enter().append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) {{ return d.name }})

    // Obnoxious as it is, you are essentially doubling the text to create a white background
    // now you will have to add it to tick to simulate movement
    const text2 = text1
        .clone(true).lower()
        .attr("fill", "none")
        .attr("stroke", "white")
        .attr("stroke-width", 3);


    //document.getElementById("dev").innerHTML = labels
    //document.getElementById("dev").innerHTML += typeof graphData.nodes.map(d => d.name)


    // Dragging functionality for nodes
    function drag(simulation) {{
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}
        
        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}
        
        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}
        
        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }}


    // This is Very Important; If you don't add this function there will be no coordinate
    // Update positions of nodes and links on each tick
    simulation.on("tick", () => {{
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        text1.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        text2.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
    }});

    
    {__zoom_js_v2}
    </script>
    """

    return html_code_2