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
            'header':'Your speaker is Ready',
            'sub_header': 'Let\'s get started',
            'done_button': 'Done'
        };
    }
    else if(lan == 'ch')
    {
        trans = {
            'header':'您的音箱已就緒',
            'sub_header': '準備開始享受您與小絨的完美旅程!',
            'done_button': '完成設定'
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