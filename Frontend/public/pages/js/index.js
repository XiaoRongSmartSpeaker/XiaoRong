document.querySelector("#start_button").addEventListener('click', function(){
    
    // fetch setting api to get the status of the speaker 
    fetch('settingAPI')
    .then(response => response.json())
    .then(speaker => {
        // user had already set the speaker
        if(speaker.status)
        {
            //redirect to done.html
            window.location.href = "done.html";
        }
        else
        {
            //redirect to wifi.html
            window.location.href = "wifi.html";
        }
    })
    .catch((error) => {
        console.log(error);
        
    })
});

