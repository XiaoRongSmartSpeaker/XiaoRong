var lan = 'ch';
var language = {
  "en":{
        'header':'Setup your XiaoRong',
        'label_language': 'Language',
        'language': '<option>English</option><option>中文</option><option>한국인</option>',
        'label_location': 'Location',
        'location': '<option>Taiwan</option><option>Japan</option><option>Korea</option>',
        'label_timezone': 'Timezone',
        'label_speaker_name': 'Name',
        'next_button': 'Next'
  },
  "ch":{
        'header':'設定您的小絨',
        'label_language': '語言',
        'language': '<option>中文</option><option>English</option><option>한국인</option>',
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
function post_info(location, language, time, speaker_name)
{
  fetch('http://localhost:3000/speaker_info', {
    method: 'POST',
    body: JSON.stringify({
      location: location,
      language: language,
      time: time,
      speaker_name: speaker_name,
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
    var language = document.querySelector("#language").value;
    var time = document.querySelector("#time").value;


    //post info to API
    post_info(location, language, time, speaker_name)
    console.log(location, language, time, speaker_name);

});