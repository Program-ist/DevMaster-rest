var colle = document.getElementsByClassName("proo_func_class");
var i = 0;
va = "func_"
for(i = 0; i < colle.length; i++){
    colle[i].id = "func_"+ i.toString();
    console.log("hello from for loop") ;
}

console.log(colle);