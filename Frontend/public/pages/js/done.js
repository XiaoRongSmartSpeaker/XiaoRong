var lan = 'ch';
var language = {
    "en":{
        'header':'Your speaker is Ready',
        'sub_header': 'Let\'s get started',
        'done_button': 'Done'
    },
    "ch":{
        'header':'您的音箱已就緒',
        'sub_header': '準備開始享受您與小絨的完美旅程!',
        'done_button': '完成設定'
    },
};
window.onload = function(){
    get_lan();
}
function get_lan()
{
    const params = new URLSearchParams(window.location.search);
    let trans = {};
    
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

