var ScriptFile={
    CreateMain:function(){
        var root=document.getElementById("jsaside");
        var find=document.getElementById("article");
        var next=find.getElementsByTagName("h2");
        for(var i=0;i<next.length;i++){
            next[i].id="jump"+i;
            var newli=document.createElement("li");
            var newa=document.createElement("a");
            newa.href="#jump"+i;
            newa.innerText=(i+1)+" "+next[i].innerText;
            newli.appendChild(newa);
            newli.classList.add("ilaside");
            root.appendChild(newli);
        }

    },
};
window.onload=function(){
        ScriptFile.CreateMain();
}