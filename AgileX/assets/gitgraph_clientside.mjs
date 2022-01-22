console.log("gitgraph_clientside.js");

let expfile = "export.json";
let path = "../static/Modules/";

setTimeout(() => {
    var elements = document.getElementsByClassName("graph-container");
    var nElements = elements.length;
    console.log("nElements:", nElements);

    Array.prototype.forEach.call(elements, element => {
        gitgraph(element);
    });

    function gitgraph_function(data, instance, idstring) {

        const metroTemplate2 = GitgraphJS.templateExtend(GitgraphJS.TemplateName.Metro, {
            commit: {
                div_id: instance,
                message: {
                    displayAuthor: false,
                    color: 'black',
                    font: 'Kiona',
                },
                dot: {
                    font: 'Kiona',
                    size: 12,
                },
                spacing: 40,
            },
            branch: {
                label: {
                    bgColor: 'black',
                    color: 'white',
                    font: 'Kiona',
                },
            },
        });

        const graphContainer = document.getElementById(idstring);
        console.log(graphContainer);
        const gitgraph = GitgraphJS.createGitgraph(graphContainer, {
            'orientation': 'vertical-reverse',
            template: metroTemplate2,
            mode: GitgraphJS.Mode.Compact,
        });
        gitgraph.import(data);

    }

    function gitgraph(element) {
        var idstring = element.id;
        var id = JSON.parse(idstring);
        console.log(id);
        var value = "./" + path + id["instance"] + "/" + expfile;
        console.log(value);
        fetch(value, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                return response.json();
            })
            .then(data => gitgraph_function(data, id["instance"], idstring));
        // console.log(data)
        // gitgraph_function(data,idstring);
    }

}, 2000);