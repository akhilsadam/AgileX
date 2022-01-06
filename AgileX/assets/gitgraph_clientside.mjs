console.log("gitgraph_clientside.js");

let expfile = "export.json";
let path = "Modules/" ;

setTimeout(() => 
{
    var elements = document.getElementsByClassName("graph-container");
    var nElements = elements.length;
    console.log("nElements:",nElements);

    Array.prototype.forEach.call(elements, element => {
        gitgraph(element);
      });

    function gitgraph_function(data,idstring) {
        const graphContainer = document.getElementById(idstring);
        console.log(graphContainer);
        const gitgraph = GitgraphJS.createGitgraph(graphContainer, {
            orientation: Orientation.VerticalReverse,
            "template" : "metro"
        });
        gitgraph.import(data);
    }

    function gitgraph(element){
        var idstring = element.id;
        var id = JSON.parse(idstring);
        console.log(id);
        var value = "./" + path + id["instance"] + "/" + expfile;
        console.log(value);
        fetch(value,
            {
                headers : 
                { 
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            })
        .then(response => {
        return response.json();
        })
        .then(data => gitgraph_function(data,idstring));
        // console.log(data)
        // gitgraph_function(data,idstring);
    }

}, 2000);