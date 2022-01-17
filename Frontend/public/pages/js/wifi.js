var wifi_name;
var lan = 'ch';
var language = {
    "en":{
        'modal_wifi_name': 'Enter Password',
        'error_mes': 'Incorrect Password',
        'modal-title': 'Password',
        'cancel_button': 'Cancel',
        'connect_button': 'Connect',
        'ok_button': 'Ok',
        'header': 'Connect to Wi-Fi',
        'sub_header': 'Choose the Wi-Fi network you\'d like to use with your XiaoRong',
        'network': 'Networks'
    },
    "ch":{
        'modal_wifi_name': '輸入密碼',
        'error_mes': '密碼錯誤',
        'modal-title': '密碼',
        'cancel_button': '取消',
        'connect_button': '連線',
        'ok_button': '好',
        'header': '連接網路',
        'sub_header': '輸入密碼以連接 Wi-Fi',
        'network': '可用的網路'
    },
}
window.onload = function(){
    get_lan();
}

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

//After the user clicks the wifi, input password's modal pops up
function wifis_onclick()
{
    var wifis = document.querySelectorAll('#wifi');

    wifis.forEach(function(wifi) {
        console.log(wifi);
        
        wifi.addEventListener('click', function() {
            
            //Add wifi name 
            wifi_name = wifi.querySelector("#wifi_name").innerHTML;
            wifi_encry = wifi.querySelector("#wifi_name").dataset.encry;
            console.log(wifi_name, wifi_encry);
            
            if(wifi_encry == "on")
            {
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
            }
            else if(wifi_encry == "off")
            {
                //Show non-encry-spinner
                wifi.querySelector('#non-encry-spinner').style.display = "block";
                input_password(wifi_name, "", wifi_encry); 

                //Ok button onclick 
                document.querySelector('#ok_button').addEventListener('click', function() {
                    // Hide modal
                    document.querySelector('#encry_wifi_modal').style.display = "none";
                    //Hide non-encry-spinner
                    wifi.querySelector('#non-encry-spinner').style.display = "none";

                    
                });
            }
            
            

            
            
        });
        
    });
}

//fetch wifi info and show image and wifi info
function fetch_show_wifi()
{
    Show_spinner();
    
    
    fetch('http://localhost:3000/wifis')
    .then(response => response.json())
    .then(networks => {
        
        //console.log(networks);
        //console.log(networks.length);
        // Get numbers of wifis
        var total_networks = networks.length;
        
        wifi_lists = document.querySelector("#wifi_lists");
        for(let i=0; i<total_networks; i++)
        {
            //wifi signal 
            wifi_signal = Number(networks[i].Signal_level.split('/')[0]);
            wifi_encry = networks[i].Encryption_key
            //console.log(wifi_signal, wifi_encry);

            //wifi encryption == 'on
            if(wifi_encry == 'on')
            {
                // different wifi_signals has different images
                if(wifi_signal >= 75)
                {
                    
                    wifi = `<div id="wifi" class="flex items-center">
                                <div class="p-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M21.2473 10.6177L23.2 8.41943C21.6803 6.69829 19.8727 5.33319 17.8817 4.40301C15.8907 3.47282 13.7557 2.99598 11.6 3.00003C7.06633 3.00003 2.96767 5.06767 0 8.41943L6.13833 15.3406L11.6 21.5L14.5483 18.1809V14.9706C14.5483 14.4809 14.6353 14.013 14.7707 13.5668C15.2927 11.8582 16.7137 10.6177 18.415 10.6177H21.2473Z" fill="#415765"/>
                                    <path fill-rule="evenodd" clip-rule="evenodd" d="M22 16V14.5C22 13.1 20.9 12 19.5 12C18.1 12 17 13.1 17 14.5V16C16.5 16 16 16.5 16 17V21C16 21.5 16.5 22 17 22H22C22.5 22 23 21.5 23 21V17C23 16.5 22.5 16 22 16ZM21 16H18V14.5C18 13.7 18.7 13 19.5 13C20.3 13 21 13.7 21 14.5V16Z" fill="#415765"/>
                                    </svg>
                                
                                </div>
                                <div id="wifi_name" class="text-theme text-xs p-2 " data-encry=${wifi_encry}>${networks[i].SSID}</div> 
                            </div>`;
                }
                
                else if(wifi_signal >= 50)
                {
                    wifi = `<div id="wifi" class="flex items-center">
                                <div class="p-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path opacity="0.3" d="M12 3C5.30002 3 0.800024 6.7 0.400024 7L3.60002 10.9L12 21.5L15.5 17.2V14.6C15.5 12.4 16.9 10.6 18.8 9.9C19.1 9.8 19.3 9.7 19.6 9.7C19.9 9.6 20.2 9.6 20.5 9.6C20.9 9.6 21.2 9.6 21.5 9.7L23.6 7C23.2 6.7 18.7 3 12 3Z" fill="#415765"/>
                                    <path d="M23 16V14.5C23 13.1 21.9 12 20.5 12C19.1 12 18 13.1 18 14.5V16C17.5 16 17 16.5 17 17V21C17 21.5 17.5 22 18 22H23C23.5 22 24 21.5 24 21V17C24 16.5 23.5 16 23 16ZM22 16H19V14.5C19 13.7 19.7 13 20.5 13C21.3 13 22 13.7 22 14.5V16ZM12 21.5L15.5 17.2V14.6C15.5 12.4 16.9 10.6 18.8 9.9C17.3 9 14.9 8 12 8C7.2 8 4 10.6 3.5 10.9" fill="#415765"/>
                                    </svg>
                                
                                </div>
                                <div id="wifi_name" class="text-theme text-xs p-2 " data-encry=${wifi_encry}>${networks[i].SSID}</div> 
                            </div>`;
                    

                }
                else if(wifi_signal >= 25)
                {
                    wifi = `<div id="wifi" class="flex items-center">
                                <div class="p-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M23 16V14.5C23 13.1 21.9 12 20.5 12C19.1 12 18 13.1 18 14.5V16C17.5 16 17 16.5 17 17V21C17 21.5 17.5 22 18 22H23C23.5 22 24 21.5 24 21V17C24 16.5 23.5 16 23 16ZM22 16H19V14.5C19 13.7 19.7 13 20.5 13C21.3 13 22 13.7 22 14.5V16Z" fill="#415765"/>
                                    <path opacity="0.3" d="M15.5 14.5C15.5 11.7 17.7 9.5 20.5 9.5C20.9 9.5 21.2 9.5 21.5 9.6L23.6 7C23.2 6.7 18.7 3 12 3C5.30002 3 0.800024 6.7 0.400024 7L12 21.5L15.5 17.2V14.5Z" fill="#415765"/>
                                    <path d="M4.79999 12.5L12 21.5L15.5 17.1V14.5C15.5 13.2 16 12 16.9 11.1C15.6 10.5 14 10 12 10C7.89999 10 5.19999 12.2 4.79999 12.5Z" fill="#415765"/>
                                    </svg>
                                                
                                </div>
                                <div id="wifi_name" class="text-theme text-xs p-2 " data-encry=${wifi_encry}>${networks[i].SSID}</div> 
                            </div>`;
                }
                else
                {
                    wifi = `<div id="wifi" class="flex items-center">
                                <div class="p-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M23 16V14.5C23 13.1 21.9 12 20.5 12C19.1 12 18 13.1 18 14.5V16C17.5 16 17 16.5 17 17V21C17 21.5 17.5 22 18 22H23C23.5 22 24 21.5 24 21V17C24 16.5 23.5 16 23 16ZM22 16H19V14.5C19 13.7 19.7 13 20.5 13C21.3 13 22 13.7 22 14.5V16Z" fill="#415765"/>
                                    <path opacity="0.3" d="M15.5 14.5C15.5 11.7 17.7 9.5 20.5 9.5C20.9 9.5 21.2 9.5 21.5 9.6L23.6 7C23.2 6.7 18.7 3 12 3C5.29999 3 0.799994 6.7 0.399994 7L12 21.5L15.5 17.2V14.5Z" fill="#415765"/>
                                    <path d="M6.70001 14.9L12 21.5L15.5 17.2V14.6C15.5 14.4 15.5 14.1 15.6 13.9C14.7 13.4 13.4 13 12 13C9.00001 13 6.90001 14.7 6.70001 14.9Z" fill="#415765"/>
                                    </svg>
                                
                                </div>
                                <div id="wifi_name" class="text-theme text-xs p-2 " data-encry=${wifi_encry}>${networks[i].SSID}</div> 
                            </div>`;
                }  
            }
            else //wifi_encry == 'off'
            {
                if(wifi_signal >= 75)
                {
                    
                    wifi = `<div id="wifi" class="flex items-center">
                                <div class="p-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12.01 21.49L23.64 7C23.19 6.66 18.71 3 12 3C5.27999 3 0.809985 6.66 0.359985 7L11.99 21.49L12 21.5L12.01 21.49V21.49Z" fill="#415765"/>
                                    </svg>
                                </div>
                                <div id="wifi_name" class="text-theme text-xs p-2 " data-encry=${wifi_encry}>${networks[i].SSID}</div> 
                                <div id="non-encry-spinner" hidden>
                                    <div class="ml-40 animate-spin rounded-full h-4 w-4 border-b-2 border-theme"></div>
                                </div>
                            </div>`;
                }
                
                else if(wifi_signal >= 50)
                {
                    wifi = `<div id="wifi" class="flex items-center">
                                <div class="p-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12.01 21.49L23.64 7C23.19 6.66 18.71 3 12 3C5.27999 3 0.809985 6.66 0.359985 7L11.99 21.49L12 21.5L12.01 21.49V21.49Z" fill="#415765" fill-opacity="0.3"/>
                                    <path d="M3.53003 10.95L11.99 21.49L12 21.5L12.01 21.49L20.47 10.95C20.04 10.62 16.81 8 12 8C7.19003 8 3.96003 10.62 3.53003 10.95V10.95Z" fill="#415765"/>
                                    </svg>
                                
                                </div>
                                <div id="wifi_name" class="text-theme text-xs p-2 " data-encry=${wifi_encry}>${networks[i].SSID}</div> 
                                <div id="non-encry-spinner" hidden>
                                    <div class="ml-40 animate-spin rounded-full h-4 w-4 border-b-2 border-theme"></div>
                                </div>
                            </div>`;
                    

                }
                else if(wifi_signal >= 25)
                {
                    wifi = `<div id="wifi" class="flex items-center">
                                <div class="p-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12.01 21.49L23.64 7C23.19 6.66 18.71 3 12 3C5.27999 3 0.809985 6.66 0.359985 7L11.99 21.49L12 21.5L12.01 21.49V21.49Z" fill="#415765" fill-opacity="0.3"/>
                                    <path d="M4.78998 12.52L11.99 21.5H12L12.01 21.49L19.21 12.51C18.85 12.24 16.1 10 12 10C7.89998 10 5.14998 12.24 4.78998 12.52Z" fill="#415765"/>
                                    </svg>
                                              
                                </div>
                                <div id="wifi_name" class="text-theme text-xs p-2 " data-encry=${wifi_encry}>${networks[i].SSID}</div> 
                                <div id="non-encry-spinner" hidden>
                                    <div class="ml-40 animate-spin rounded-full h-4 w-4 border-b-2 border-theme"></div>
                                </div>
                            </div>`;
                }
                else
                {
                    wifi = `<div id="wifi" class="flex items-center">
                                <div class="p-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12.01 21.49L23.64 7C23.19 6.66 18.71 3 12 3C5.27999 3 0.809985 6.66 0.359985 7L11.99 21.49L12 21.5L12.01 21.49V21.49Z" fill="#415765" fill-opacity="0.3"/>
                                    <path d="M6.66998 14.86L12 21.49V21.5L12.01 21.49L17.34 14.86C17.06 14.65 15.03 13 12 13C8.96998 13 6.93998 14.65 6.66998 14.86Z" fill="#415765"/>
                                    </svg>
                                
                                </div>
                                <div id="wifi_name" class="text-theme text-xs p-2 " data-encry=${wifi_encry}>${networks[i].SSID}</div> 
                                <div id="non-encry-spinner" hidden>
                                    <div class="ml-40 animate-spin rounded-full h-4 w-4 border-b-2 border-theme"></div>
                                </div>
                            </div>`;
                }  
            }

            
            // add to wifi lists
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

//post wifi info to api, wifi with password or without password depends on wifi encryption
function input_password(wifi_name, pw, wifi_encry)
{
    
    console.log(wifi_name + pw);

    if(wifi_encry == "on")
    {
        // Show loading spinner
        document.querySelector('#connect_spinner').style.display = "block"; 
    }
    
    

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
    .then(isConnected => {
        console.log(isConnected);
        
        //if success, then redirect to google signin page
        if(isConnected)
        {
            window.location.href = `signin.html?lan=${lan}`;
        }
        //if error, show error message ,clear input form and hide connect spinner
        else
        {
            if(wifi_encry == "on")
            {
                document.querySelector('#error_mes').style.display = "block";
                document.querySelector("#password").value = "";
                document.querySelector('#connect_spinner').style.display = "none";  
            }
            else if(wifi_encry == "off")
            {
                // Set error message
                error_mes = `無法連接${wifi_name}`;
                if(lan == 'en')
                {
                    error_mes = `Failed to connect to ${wifi_name}`;
                }
                document.querySelector('#encry_wifi_error_mes').innerHTML = error_mes;

                // Show modal
                document.querySelector('#encry_wifi_modal').style.display = "block";

                

            }
            
        }

    })
    .catch((error) => {
        console.error('Error:', error);
    });
    

    
    
    
    

}

// Get language and set language
function get_lan()
{
    const params = new URLSearchParams(window.location.search);
    var trans = {};
    
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

    

}

//get_lan();
document.addEventListener('DOMContentLoaded', function(){
    fetch_show_wifi();
    
    // Refresh button onclick then fetch again
    document.querySelector('#refresh_button').addEventListener('click', () => {

        // Clear wifi_lists innerHTMl
        document.querySelector("#wifi_lists").innerHTML = "";

        // Fetch wifi API
        fetch_show_wifi();
        
       
    
    
    });
})

//Connect button onclick then post wifi info to api
document.querySelector('#connect_button').addEventListener('click', () => {
                
    // Get the password
    const pw = document.querySelector("#password").value;
    
    input_password(wifi_name, pw, "on");  
    

    
});