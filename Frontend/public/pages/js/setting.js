function post_info(location, speaker_name)
{
  fetch('API', {
    method: 'POST',
    body: JSON.stringify({
      location: location,
      speaker_name: speaker_name,
    })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);

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
        speaker_name = "小絨音箱";
    }
    // get location
    var location = document.querySelector("#location").value;

    //post info to API
    post_info(location, speaker_name)
    console.log(location, speaker_name);

});