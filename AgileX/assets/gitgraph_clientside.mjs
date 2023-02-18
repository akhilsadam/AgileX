console.log("gitgraph_clientside.js");

let expfile = "export.json";
let path = "../static/Modules/";

setTimeout(() => {
    var elements = document.getElementsByClassName("graph-container");
    var nElements = elements.length;
    // console.log("nElements:", nElements);

    Array.prototype.forEach.call(elements, element => {
        gitgraph(element);
    });

    var compareBranchesOrder = function(a, b) {
        return (a - b);
    };

    function gitgraph_function(data, instance, idstring) {

        const metroTemplate2 = GitgraphJS.templateExtend(GitgraphJS.TemplateName.Metro, {
            colors: ["rgb(23,20,18)", "rgb(143,29,33)", "rgb(25,31,69)", "rgb(49, 117, 137)", "rgb(120, 119, 155)", "rgb(226,177,60)"],
            //  kokushoku, shinshu, konkikyo, chigusa-iro, benimidori, kariyasu,
            commit: {
                div_id: instance,
                message: {
                    displayAuthor: false,
                    color: 'rgb(23, 20, 18)',
                    font: 'Kiona',
                },
                dot: {
                    font: 'Kiona',
                    size: 12,
                },
                style: {

                },
                spacing: 40,
            },
            branch: {
                label: {
                    bgColor: 'var(--strokeColor)',
                    // strokeColor: 'rgb(23, 20, 18)',
                    color: 'white',
                    font: 'Kiona',
                },
            },
        });

        const graphContainer = document.getElementById(idstring);
        // console.log(graphContainer);
        const gitgraph = GitgraphJS.createGitgraph(graphContainer, {
            'orientation': 'vertical-reverse',
            template: metroTemplate2,
            mode: GitgraphJS.Mode.Compact,
            compareBranchesOrder: compareBranchesOrder,
        });
        gitgraph.import(data);
        // console.log(data);
        // find head
        data.every(element => {
            if (element.refs[0] == "HEAD") {
                gitgraph._graph.tags.set("HEAD", element.hash);
                return false;
            }
            return true;
        })
    }

    function gitgraph(element) {
        var idstring = element.id;
        var id = JSON.parse(idstring);
        // console.log(id);
        var value = "./" + path + id["instance"] + "/" + expfile;
        // console.log(value);
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