let newId = 0;
let subjectNames = [];
let subjectCounts = [];
var dragged;

let param = 0;

// the div only triggers a change
function dummy2(numb) {
    let id = numb.currentTarget.id.substr(2);
    subjectNames[id] = document.getElementById('subjectName' + id).value;
    subjectCounts[id] = document.getElementById('subjectCount' + id).value;
    // console.log(subjectCounts);
    // console.log(subjectNames);
}

function addSubject() {
    
    // creating new default values in the arrays for storing the info of the new subject 
    subjectCounts.push(0);
    subjectNames.push('');

    // // Container <div> where dynamic content will be placed
    var container = document.getElementById("container");
    
    // creating a div for this element
    var div = document.createElement("div");
    div.id = 'id' + newId;
    div.addEventListener("change", dummy2); // what to do when any part of the div changes

    var subjectName = document.createElement("input");
    subjectName.type = 'text';
    subjectName.id = 'subjectName'+newId;
    subjectName.name = 'subjectName'+newId;
    subjectName.placeholder = 'Subject Name';
    
    // Create an <input> element, set its type and name attributes
    var subjectCount = document.createElement("input");
    subjectCount.type = "number";
    subjectCount.id = 'subjectCount'+newId;
    subjectCount.name = 'subjectCount'+newId;
    subjectCount.placeholder = 'No of persiods/week'; 
    
    newId += 1;

    div.appendChild(subjectName);
    div.appendChild(subjectCount);

    container.appendChild(div);
    // Append a line break 
    container.appendChild(document.createElement("br"));
}

function createTable() {
    let sum = 0, one;
    for (let i = 0 ; i < newId ; i++) {
        one = parseInt(subjectCounts[i]);
        if (one < 1) {
            alert("Please enter a positive number of periods for the " + subjectNames[i] + " subject."); 
            return;
        }
        if (isNaN(one)) {
            alert("Please enter the number of periods for the " + subjectNames[i] + " subject."); 
            return;
        }
        sum += one;
    }
    if (sum != 42){
        alert("The total number of periods must be 42");
        return; 
    }
    let uniqueSubjectNames = new Set(subjectNames);
    if (uniqueSubjectNames.size != subjectNames.length) {
        alert("Each subject name must be unique"); 
        return;
    }
    else {

        var container = document.getElementById("container");
        
        let foo = document.createTextNode("You can drag and swap the periods!");
        container.appendChild(foo);

        let counter = 0, index = 0, max = parseInt(subjectCounts[index]);
        let table = document.createElement("div");
        for (let i = 0 ; i < 9 ; ++i) {
            var row = document.createElement("div");
            row.className = "row";
            for (let j = 0 ; j < 5 ; ++j) {
                if (counter == max) {
                    index += 1;
                    max = parseInt(subjectCounts[index]);
                    counter = 0;
                }
                var dnd = document.createElement("div");
                dnd.className = "dnd";
                dnd.id = "dnd" + i + j;
                dnd.draggable = true;
                // dnd.ondragstart = event.dataTransfer.setData('text/plain',null);
                dnd.id = "drag" + i + j;
                dnd.textContent = subjectNames[index];
                row.appendChild(dnd);
                counter += 1;
                if (i > 5 && j == 3) {
                  break;
                }
            }
            table.appendChild(row);
        }
        container.appendChild(table);
    }
}


/* events fired on the draggable target */
document.addEventListener("drag", function(event) {

}, false);

document.addEventListener("dragstart", function(event) {
  // store a ref. on the dragged elem
  dragged = event.target;
  // make it half transparent
//   event.target.style.opacity = .5;
}, false);

document.addEventListener("dragend", function(event) {
  // reset the transparency
//   event.target.style.opacity = "";
}, false);

/* events fired on the drop targets */
document.addEventListener("dragover", function(event) {
  // prevent default to allow drop
  event.preventDefault();
}, false);

document.addEventListener("dragenter", function(event) {
  // highlight potential drop target when the draggable element enters it
  if (event.target.className == "dropzone") {
    // event.target.style.background = "purple";
  }

}, false);

document.addEventListener("dragleave", function(event) {
  // reset background of potential drop target when the draggable element leaves it
  if (event.target.className == "dropzone") {
    // event.target.style.background = "";
  }

}, false);

document.addEventListener("drop", function(event) {
  // prevent default action (open as link for some elements)
  event.preventDefault();
  // move dragged elem to the selected drop target
  // target is a button; button <- drag <- drop
  if (event.target.className == "dnd") {
    
    var temp = event.target.textContent;
    event.target.textContent = dragged.textContent;
    dragged.textContent = temp;

    
  }
}, false);

