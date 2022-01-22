// const dash_prefix = '/dashapp/';
// // already declared
// // const reg = "/static/Modules/";
// // const WT = "/static/ModuleWT/";
// // const ext = ".txt";
// // const itemid_prefix = "autosave_";

// const downloadToFile = (content, filename, contentType) => {
//     const a = document.createElement('a');
//     const file = new Blob([content], {type: contentType});
    
//     a.href= URL.createObjectURL(file);
//     a.download = filename;
//     a.click();

//     URL.revokeObjectURL(a.href);
// };


// setTimeout(() => 
// {

//     // const fs = require("fs");
//     // console.log(fs);

//     var elements = document.getElementsByClassName("module-input-change"); //document.getElementsByClassName("module-save");
//     var nElements = elements.length;
//     console.log("nElements:",nElements);

//     Array.prototype.forEach.call(elements, element => {
//         codemir(element);
//       });

//     function codemir(element){
//         var idstring = element.id;
//         var id = JSON.parse(idstring);
//         console.log(id);

//         // var itemid = itemid_prefix + id;

//         // var originalDiv = ('#'+"{'type':'module-input-code','instance':"+idn+"}"); 
//         // var editor = originalDiv.next('.CodeMirror')[0].CodeMirror;
//         // const selectElement = document.getElementById(idstr);


//         // window.onload = function() {
//         //     var dataf = document.getElementsByClassName("module-input-code")[id['instance']];
//         //     if (sessionStorage.getItem(itemid))
//         //         dataf.value = sessionStorage.getItem(itemid);
//         // }

//         element.addEventListener('keyup', (event) => { //keyup

//             var idn = id['instance'];
//             var elements2 = document.getElementsByClassName("CodeMirror")[idn];
//             var dataf = document.getElementsByClassName("module-input-code")[idn];

//             console.log(elements2);
//             var text = elements2.CodeMirror.doc.getValue();
        
//             dataf.innerText = text;
//             dataf.setAttribute('value',text);
//             dataf.value = text;
//             console.log("Changed",dataf);

//             // var address = reg + idn + '/' + idn + ext;
//             // console.log("Address: ",address,"Text: ",text);

//             // fs.writeFile(address, text, "utf8", (error, data) => {
//             //     console.log("Write complete");
//             //     console.log(error);
//             //     console.log(data);
//             // });

//             //downloadToFile(text, address, 'text/plain');

//             // sessionStorage.setItem(itemid, dataf.value);

//         });
        
//         // gitgraph_function(data,idstring);
//     }

// }, 2000);
