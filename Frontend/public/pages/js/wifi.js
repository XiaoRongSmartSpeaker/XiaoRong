var wifi_name;

function Show_spinner()
{
    // Hide refresh button, show loading spinner
   const refresh_button = document.querySelector('#refresh_button');
   const loading_spinner = document.querySelector('#loading_spinner');
   
    refresh_button.style.display = 'none';
    loading_spinner.style.display = 'block';
    
   //refresh_button.hidden = true;
    
   //loading_spinner.hidden = false;
}
function Hide_spinner()
{
    
    const refresh_button = document.querySelector('#refresh_button');
    const loading_spinner = document.querySelector('#loading_spinner');
    refresh_button.style.display = 'block';
    loading_spinner.style.display = 'none';
    //refresh_button.hidden = false;


    //loading_spinner.hidden = true;
}

function wifis_onclick()
{
    var wifis = document.querySelectorAll('#wifi');

    wifis.forEach(function(wifi) {
        console.log(wifi);
        
        wifi.addEventListener('click', function() {
            
            //Add wifi name 
            wifi_name = wifi.querySelector("#wifi_name").innerHTML;
            console.log(wifi_name);

            document.querySelector('#modal_wifi_name').innerHTML = `輸入${wifi_name}的密碼`;

            //Show input modal
            document.querySelector('#wifi_modal').style.display = "block";

            //Cancel button onclick 
            document.querySelector('#cancel_button').addEventListener('click', function() {
                // Hide input modal
                document.querySelector('#wifi_modal').style.display = "none";
                //Hide "wrong password"
                document.querySelector('#error_mes').style.display = "none";

                
            });

            
            
        });
        
    });
}

function fetch_show_wifi()
{
    Show_spinner();
    
    
    fetch('http://localhost:3000/wifis')
    .then(response => response.json())
    .then(networks => {
        
        console.log(networks);
        console.log(networks.length);
        // Get numbers of wifis
        var total_networks = networks.length;
        
        wifi_lists = document.querySelector("#wifi_lists");
        for(let i=0; i<total_networks; i++)
        {
            //wifi signal strong
            if(networks[i].signal > 100)
            {
                wifi = `<div id="wifi" class="flex items-center"><div class="p-3"><svg class="" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18.3167 9.1666L20 7.48327C18.6899 6.16528 17.1317 5.11994 15.4153 4.40763C13.6989 3.69532 11.8583 3.33017 10 3.33327C6.09167 3.33327 2.55833 4.9166 0 7.48327L5.29167 12.7833L10 17.4999L12.5417 14.9583V12.4999C12.5417 12.1249 12.6167 11.7666 12.7333 11.4249C13.1833 10.1166 14.4083 9.1666 15.875 9.1666H18.3167Z" fill="#415765"/>
                <path d="M18.3332 13.3334V12.5C18.3332 11.5834 17.5832 10.8334 16.6665 10.8334C15.7498 10.8334 14.9998 11.5834 14.9998 12.5V13.3334C14.5415 13.3334 14.1665 13.7084 14.1665 14.1667V16.6667C14.1665 17.125 14.5415 17.5 14.9998 17.5H18.3332C18.7915 17.5 19.1665 17.125 19.1665 16.6667V14.1667C19.1665 13.7084 18.7915 13.3334 18.3332 13.3334ZM17.4998 13.3334H15.8332V12.5C15.8332 12.0417 16.2082 11.6667 16.6665 11.6667C17.1248 11.6667 17.4998 12.0417 17.4998 12.5V13.3334Z" fill="#415765">
                </svg></div><div id="wifi_name" class="text-theme text-xs p-2 ">${networks[i].name}</div> </div>`;
            }
            // wifi signal weak
            else
            {
                wifi = `<div id="wifi" class="flex items-center"><div class="p-3"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19.1665 10V8.875C19.1665 7.825 18.2498 7 17.0832 7C15.9165 7 14.9998 7.825 14.9998 8.875V10C14.5832 10 14.1665 10.375 14.1665 10.75V13.75C14.1665 14.125 14.5832 14.5 14.9998 14.5H19.1665C19.5832 14.5 19.9998 14.125 19.9998 13.75V10.75C19.9998 10.375 19.5832 10 19.1665 10ZM18.3332 10H15.8332V8.875C15.8332 8.275 16.4165 7.75 17.0832 7.75C17.7498 7.75 18.3332 8.275 18.3332 8.875V10Z" fill="#415765"/>
                <path opacity="0.3" d="M12.9163 8.875C12.9163 6.775 14.7497 5.125 17.083 5.125C17.4163 5.125 17.6663 5.125 17.9163 5.2L19.6663 3.25C19.333 3.025 15.583 0.25 9.99967 0.25C4.41634 0.25 0.666341 3.025 0.333008 3.25L9.99967 14.125L12.9163 10.9V8.875Z" fill="#415765"/>
                <path d="M4 7.375L10 14.125L12.9167 10.825V8.875C12.9167 7.9 13.3333 7 14.0833 6.325C13 5.875 11.6667 5.5 10 5.5C6.58333 5.5 4.33333 7.15 4 7.375Z" fill="#415765"/>
                </svg>                
                </div><div id="wifi_name" class="text-theme text-xs p-2 ">${networks[i].name}</div> </div>`;
                

            }
            
            wifi_lists.innerHTML += wifi;
            
        }
        Hide_spinner();
    })
    .then(() => {
        wifis_onclick();
    })
    .catch((error) => {
        console.log(error);
        
    })
    

}

function input_password(wifi_name, pw)
{
    
    console.log(wifi_name + pw);

    // Show loading spinner
    document.querySelector('#connect_spinner').style.display = "block";

    //Post pw to api
    fetch('http://localhost:3000/setting_wifi', {
        method: 'PUT',
        body: JSON.stringify({
          SSID: wifi_name,
          password: pw,
         
        }),
        headers: {'Content-Type': 'application/json'}
      })
    .then(response => response.json())
    .then(connect => {
        console.log(connect);

        //if success, then redirect to google signin page
        if(connect == "success")
        {
            window.location.href = "signin.html";
        }
        //if error, show error message ,clear input form and hide connect spinner
        else
        {
            document.querySelector('#error_mes').style.display = "block";
            document.querySelector("#password").value = "";
            document.querySelector('#connect_spinner').style.display = "none";
        }

    })
    .catch((error) => {
        console.error('Error:', error);
    });
    

    
    
    
    

}


document.addEventListener('DOMContentLoaded', function(){
    fetch_show_wifi();
    
    // Refresh button onclick (Not showing spinner?)
    document.querySelector('#refresh_button').addEventListener('click', () => {

        // Clear wifi_lists innerHTMl
        document.querySelector("#wifi_lists").innerHTML = "";

        // Fetch wifi API
        fetch_show_wifi();
        
       
    
    
    });
})

//Connect button onclick
document.querySelector('#connect_button').addEventListener('click', () => {
                
    // Get the password
    const pw = document.querySelector("#password").value;
    
    input_password(wifi_name, pw);  
    

    
});