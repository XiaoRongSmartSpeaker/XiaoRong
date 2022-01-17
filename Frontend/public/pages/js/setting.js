var lan = 'ch';
var language = {
  "en":{
        'header':'Setup your XiaoRong',
        'label_location': 'Location',
        'location': '<option>Taiwan</option><option>Japan</option><option>Korea</option>',
        'label_timezone': 'Timezone',
        'label_speaker_name': 'Name',
        'next_button': 'Next'
  },
  "ch":{
        'header':'設定您的小絨',
        'label_location': '地區',
        'location': '<option>台灣</option><option>日本</option><option>韓國</option>',
        'label_timezone': '時區',
        'label_speaker_name': '名稱',
        'next_button': '下一步'
  },
}
window.onload = function(){
  get_lan();
}
const urlObj = new URL(document.URL)
let flask_base_url= urlObj.protocol + "//" + urlObj.hostname;

if(urlObj.port != undefined)
{
  flask_base_url = flask_base_url.concat(":" + urlObj.port);
}


function get_lan()
{
    const params = new URLSearchParams(window.location.search);
    var trans = {};
    
    if(params.has('lan'))
    {
        lan = params.get('lan');
    }
    trans = language[lan];
    
    if(lan == 'en')
    {
      // Update placeholder of input form
      document.getElementById('speaker_name').placeholder = "XiaoRong speaker";
    }
    else if(lan == 'ch')
    {
      // Update placeholder of input form
      document.getElementById('speaker_name').placeholder = "小絨音箱";
    }
    

    // Set language
    for(let key in trans)
    {
        document.getElementById(key).innerHTML = trans[key];
    }

    console.log(params.has('lan'));

}

//get_lan();
function post_info(location, time, speaker_name)
{
  fetch(flask_base_url +'/speaker_info', {
    method: 'POST',
    body: JSON.stringify({
      location: location,
      time: time,
      speaker_name: speaker_name,
      language: lan
    }),
    headers: {'Content-Type': 'application/json'}
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
    window.location.href = `done.html?lan=${lan}`;

  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

document.querySelector("button").addEventListener("click", () => {
    //get speaker's name
    var speaker_name = document.querySelector("#speaker_name").value;

    // check if speaker_name contains all white spaces
    var all_white_spaces = true;
    for(let i=0; i<speaker_name.length; i++)
    {
        if(speaker_name[i] != ' ')
        {
            all_white_spaces = false;
            break;
        }
    }
    if(speaker_name == "" || all_white_spaces)
    {
        speaker_name = document.getElementById('speaker_name').placeholder;
    }

    // get location
    var location = document.querySelector("#location").value;
    
    var time = document.querySelector("#time").value;


    //post info to API
    post_info(location, time, speaker_name)
    
});