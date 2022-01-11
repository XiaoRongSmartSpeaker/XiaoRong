var language = {
    "en":{
        'start_button':'Start',
        'language': '<a href="?lan=ch">中文</a>'
    },
    "ch":{
        'start_button':'開始使用',
        'language': '<a href="?lan=en">English</a>'
    },
}
window.onload = function(){
    get_lan();
}
let lan = 'ch';
function get_lan()
{
    const params = new URLSearchParams(window.location.search);
    var trans = {};
    
    if(params.has('lan'))
    {
        lan = params.get('lan');
    }
    
    trans = language[lan];

    // Set language
    for(let key in trans)
    {
        document.getElementById(key).innerHTML = trans[key];
    }

    console.log(params.has('lan'));

}


document.getElementById('start_button').addEventListener('click', () => {
   
    
    window.location.href = `wifi.html?lan=${lan}`;
});