console.log("innn");
let lan = 'ch';
function get_lan()
{
    const params = new URLSearchParams(window.location.search);
    var trans = {};
    
    if(params.has('lan'))
    {
        lan = params.get('lan');
    }
    

    if(lan == 'en')
    {
        trans = {
            'start_button':'Start',
            'language': '<a href="?lan=ch">中文</a>'
        };
    }
    else if(lan == 'ch')
    {
        trans = {
            'start_button':'開始使用',
            'language': '<a href="?lan=en">English</a>'
        };
    }

    // Set language
    for(var key in trans)
    {
        document.getElementById(key).innerHTML = trans[key];
    }

    console.log(params.has('lan'));

}

get_lan();
document.getElementById('start_button').addEventListener('click', () => {
    console.log(lan);
    
    window.location.href = `wifi.html?lan=${lan}`;
});