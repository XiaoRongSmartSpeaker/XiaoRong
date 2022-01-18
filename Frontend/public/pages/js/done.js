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
const urlObj = new URL(document.URL);
let flask_base_url = urlObj.protocol + '//' + urlObj.hostname;

if (urlObj.port != undefined) {
  flask_base_url = flask_base_url.concat(':' + urlObj.port);
}

window.onload = function(){
    get_lan();
    fetch(flask_base_url + '/done')
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

