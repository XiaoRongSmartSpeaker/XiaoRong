var wifi_name;
let lan = 'ch';

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

            if(lan == 'en')
            {
                document.querySelector('#modal_wifi_name').innerHTML = `Enter the password for ${wifi_name}`;
            }
            else if(lan == 'ch')
            {
                document.querySelector('#modal_wifi_name').innerHTML = `輸入${wifi_name}的密碼`;
            }
            

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
            //wifi signal 
            if(networks[i].signal >= 75)
            {
                wifi = `<div id="wifi" class="flex items-center"><div class="p-3"><svg class="" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18.3167 9.1666L20 7.48327C18.6899 6.16528 17.1317 5.11994 15.4153 4.40763C13.6989 3.69532 11.8583 3.33017 10 3.33327C6.09167 3.33327 2.55833 4.9166 0 7.48327L5.29167 12.7833L10 17.4999L12.5417 14.9583V12.4999C12.5417 12.1249 12.6167 11.7666 12.7333 11.4249C13.1833 10.1166 14.4083 9.1666 15.875 9.1666H18.3167Z" fill="#415765"/>
                <path d="M18.3332 13.3334V12.5C18.3332 11.5834 17.5832 10.8334 16.6665 10.8334C15.7498 10.8334 14.9998 11.5834 14.9998 12.5V13.3334C14.5415 13.3334 14.1665 13.7084 14.1665 14.1667V16.6667C14.1665 17.125 14.5415 17.5 14.9998 17.5H18.3332C18.7915 17.5 19.1665 17.125 19.1665 16.6667V14.1667C19.1665 13.7084 18.7915 13.3334 18.3332 13.3334ZM17.4998 13.3334H15.8332V12.5C15.8332 12.0417 16.2082 11.6667 16.6665 11.6667C17.1248 11.6667 17.4998 12.0417 17.4998 12.5V13.3334Z" fill="#415765">
                </svg></div><div id="wifi_name" class="text-theme text-xs p-2 ">${networks[i].name}</div> </div>`;
            }
            
            else if(networks[i].signal >= 50)
            {
                wifi = `<div id="wifi" class="flex items-center"><div class="p-3"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path opacity="0.3" d="M9.50023 2.375C4.19606 2.375 0.633561 5.30417 0.316895 5.54167L2.85023 8.62917L9.50023 17.0208L12.2711 13.6167V11.5583C12.2711 9.81667 13.3794 8.39167 14.8836 7.8375C15.1211 7.75833 15.2794 7.67917 15.5169 7.67917C15.7544 7.6 15.9919 7.6 16.2294 7.6C16.5461 7.6 16.7836 7.6 17.0211 7.67917L18.6836 5.54167C18.3669 5.30417 14.8044 2.375 9.50023 2.375V2.375Z" fill="#415765"/>
                <path d="M18.2085 12.6667V11.4792C18.2085 10.3709 17.3377 9.50004 16.2293 9.50004C15.121 9.50004 14.2502 10.3709 14.2502 11.4792V12.6667C13.8543 12.6667 13.4585 13.0625 13.4585 13.4584V16.625C13.4585 17.0209 13.8543 17.4167 14.2502 17.4167H18.2085C18.6043 17.4167 19.0002 17.0209 19.0002 16.625V13.4584C19.0002 13.0625 18.6043 12.6667 18.2085 12.6667ZM17.4168 12.6667H15.0418V11.4792C15.0418 10.8459 15.596 10.2917 16.2293 10.2917C16.8627 10.2917 17.4168 10.8459 17.4168 11.4792V12.6667ZM9.50016 17.0209L12.271 13.6167V11.5584C12.271 9.81671 13.3793 8.39171 14.8835 7.83754C13.696 7.12504 11.796 6.33337 9.50016 6.33337C5.70016 6.33337 3.16683 8.39171 2.771 8.62921" fill="#415765"/>
                </svg>
                
                
                </div><div id="wifi_name" class="text-theme text-xs p-2 ">${networks[i].name}</div> </div>`;
                

            }
            else if(networks[i].signal >= 25)
            {
                wifi = `<div id="wifi" class="flex items-center"><div class="p-3"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19.1665 10V8.875C19.1665 7.825 18.2498 7 17.0832 7C15.9165 7 14.9998 7.825 14.9998 8.875V10C14.5832 10 14.1665 10.375 14.1665 10.75V13.75C14.1665 14.125 14.5832 14.5 14.9998 14.5H19.1665C19.5832 14.5 19.9998 14.125 19.9998 13.75V10.75C19.9998 10.375 19.5832 10 19.1665 10ZM18.3332 10H15.8332V8.875C15.8332 8.275 16.4165 7.75 17.0832 7.75C17.7498 7.75 18.3332 8.275 18.3332 8.875V10Z" fill="#415765"/>
                <path opacity="0.3" d="M12.9163 8.875C12.9163 6.775 14.7497 5.125 17.083 5.125C17.4163 5.125 17.6663 5.125 17.9163 5.2L19.6663 3.25C19.333 3.025 15.583 0.25 9.99967 0.25C4.41634 0.25 0.666341 3.025 0.333008 3.25L9.99967 14.125L12.9163 10.9V8.875Z" fill="#415765"/>
                <path d="M4 7.375L10 14.125L12.9167 10.825V8.875C12.9167 7.9 13.3333 7 14.0833 6.325C13 5.875 11.6667 5.5 10 5.5C6.58333 5.5 4.33333 7.15 4 7.375Z" fill="#415765"/>
                </svg>                
                </div><div id="wifi_name" class="text-theme text-xs p-2 ">${networks[i].name}</div> </div>`;
            }
            else
            {
                wifi = `<div id="wifi" class="flex items-center"><div class="p-3"><svg width="20" height="18" viewBox="0 0 20 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19.1665 12V10.875C19.1665 9.825 18.2498 9 17.0832 9C15.9165 9 14.9998 9.825 14.9998 10.875V12C14.5832 12 14.1665 12.375 14.1665 12.75V15.75C14.1665 16.125 14.5832 16.5 14.9998 16.5H19.1665C19.5832 16.5 19.9998 16.125 19.9998 15.75V12.75C19.9998 12.375 19.5832 12 19.1665 12ZM18.3332 12H15.8332V10.875C15.8332 10.275 16.4165 9.75 17.0832 9.75C17.7498 9.75 18.3332 10.275 18.3332 10.875V12Z" fill="#415765"/>
                <path opacity="0.3" d="M12.9168 10.875C12.9168 8.775 14.7502 7.125 17.0835 7.125C17.4168 7.125 17.6668 7.125 17.9168 7.2L19.6668 5.25C19.3335 5.025 15.5835 2.25 10.0002 2.25C4.41683 2.25 0.666829 5.025 0.333496 5.25L10.0002 16.125L12.9168 12.9V10.875Z" fill="#415765"/>
                <path d="M5.5835 11.175L10.0002 16.125L12.9168 12.9V10.95C12.9168 10.8 12.9168 10.575 13.0002 10.425C12.2502 10.05 11.1668 9.75 10.0002 9.75C7.50016 9.75 5.75016 11.025 5.5835 11.175Z" fill="#415765"/>
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
            window.location.href = `signin.html?lan=${lan}`;
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
            'modal_wifi_name': 'Enter Password',
            'error_mes': 'Incorrect Password',
            'modal-title': 'Password',
            'cancel_button': 'Cancel',
            'connect_button': 'Connect',
            'header': 'Connect to Wi-Fi',
            'sub_header': 'Choose the Wi-Fi network you\'d like to use with your XiaoRong',
            'network': 'Networks'
        };
    }
    else if(lan == 'ch')
    {
        trans = {
            'modal_wifi_name': '輸入密碼',
            'error_mes': '密碼錯誤',
            'modal-title': '密碼',
            'cancel_button': '取消',
            'connect_button': '連線',
            'header': '連接網路',
            'sub_header': '輸入密碼以連接 Wi-Fi',
            'network': '可用的網路'
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