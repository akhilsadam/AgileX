alert("gitgraph_clientside.js");
setTimeout(() => 
{
    function gitgraph_function(value,id) {
        alert(value);
        alert(id);
        //var idstring = '{\"instance\":\"'+id['instance']+'\",\"type\":\"'+id['type']+'\"}';
        let idstring;
        if (!(typeof id === 'string' || id instanceof String)) 
        {
            idstring = JSON.stringify(id, Object.keys(id).sort());
        }
        else
        {
            idstring = id;
        }
        alert(id);
        import data from value;
        alert(data);
        const graphContainer = document.getElementById(idstring);
        alert(graphContainer);
        const gitgraph = GitgraphJS.createGitgraph(graphContainer, {
            "orientation": "vertical",
            "template" : "metro"
        });
        gitgraph.import(data);
    }

    function gitgraph(element){
        var id = element.id;
        console.log(id);
    }

    var elements = document.getElementsByClassName("graph-container");
    var nElements = elements.length;
    alert(nElements);
    elements.forEach(gitgraph);

}, 2000);