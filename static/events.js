 function randomString(length, chars) {
    var result = '';
    for (var i = length; i > 0; --i) result += chars[Math.floor(Math.random() * chars.length)];
    return result;
}

function generate(){
  rString = randomString(16, '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ');
  document.getElementById('copyId').value=rString;
  document.getElementById('copied').style="display:none"
}

function copyId(check){
  var e = document.getElementById('copyId')
  var t = document.getElementById('copied');
  t.style="display:block"
  if (check){
    t.innerText="Todo id already taken please generate new one."
  }
  else{
    
  if(e.value.length==0){
    t.innerText="Todo id is empty"
  }
  else{
    t.innerText="Todo id is copied, Save it for future refrences"
    e.select();
    e.setSelectionRange(0, 99999); /* For mobile devices */
    document.execCommand('copy');
  }
}
}


function listSearch(e){
  if(e.value==0){
  document.getElementById('search').style='display:form';
  e.innerText='Close';
  e.value=1;
  }
  else{
  document.getElementById('search').style='display:none';
  e.innerText='Search on a List';
  e.value=0;
  }

}

function func(pr) {
  var cls  = document.getElementsByClassName('TodoPr')
  for (let i = 0; i < 5; i++) {
   if (cls[i].value == pr)  {
     cls[i].setAttribute("checked",true)
   }
 }
}