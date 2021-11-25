function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
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
function fetch_show_wifi()
{
    Show_spinner();
    sleep(1000);

    fetch('wifiap')
    .then(response => response.json())
    .then(networks => {
        
        // Get numbers of wifis
        var total_networks = length(networks);
        
        wifi_lists = document.querySelector("#wifi_lists");
        for(let i=0; i<total_networks; i++)
        {
            wifi = `<div class="flex items-center"><div class="p-3"><svg class="" width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18.3167 9.1666L20 7.48327C18.6899 6.16528 17.1317 5.11994 15.4153 4.40763C13.6989 3.69532 11.8583 3.33017 10 3.33327C6.09167 3.33327 2.55833 4.9166 0 7.48327L5.29167 12.7833L10 17.4999L12.5417 14.9583V12.4999C12.5417 12.1249 12.6167 11.7666 12.7333 11.4249C13.1833 10.1166 14.4083 9.1666 15.875 9.1666H18.3167Z" fill="#415765"/><path d="M18.3332 13.3334V12.5C18.3332 11.5834 17.5832 10.8334 16.6665 10.8334C15.7498 10.8334 14.9998 11.5834 14.9998 12.5V13.3334C14.5415 13.3334 14.1665 13.7084 14.1665 14.1667V16.6667C14.1665 17.125 14.5415 17.5 14.9998 17.5H18.3332C18.7915 17.5 19.1665 17.125 19.1665 16.6667V14.1667C19.1665 13.7084 18.7915 13.3334 18.3332 13.3334ZM17.4998 13.3334H15.8332V12.5C15.8332 12.0417 16.2082 11.6667 16.6665 11.6667C17.1248 11.6667 17.4998 12.0417 17.4998 12.5V13.3334Z" fill="#415765"></svg></div><div class="text-theme text-xs p-2 ">${networks[i].name}</div> </div>`;
            wifi_lists.innerHTML += wifi;
            
        }
        Hide_spinner();
    })
    .catch((error) => {
        console.log(error);
        
    })
    

}
fetch_show_wifi();
// Refresh button onclick (Not showing spinner?)
document.querySelector('#refresh_button').addEventListener('click', () => {

    // Clear wifi_lists innerHTMl
    document.querySelector("#wifi_lists").innerHTML = "";

    // Fetch wifi API
    fetch_show_wifi();

   
   
});
function input_password(wifi_name)
{
    //Get the password 
    const pw = document.querySelector("#password").value;
    console.log(wifi_name + pw);

    // Show loading spinner
    document.querySelector('#connect_spinner').style.display = "block";

    //Post to api
    fetch('API', {
        method: 'POST',
        body: JSON.stringify({
          name: wifi_name,
          password: pw,
        })
      })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        //if success, then redirect to google signin page
        if(data == "success")
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

document.querySelectorAll('#wifi').forEach(wifi => {
    //console.log(wifi);
    wifi.addEventListener('click', function() {
        
        //Add wifi name 
        var wifi_name = wifi.querySelector("#wifi_name").innerHTML;
        //console.log(wifi_name);

        document.querySelector('#modal_wifi_name').innerHTML = `輸入${wifi_name}的密碼`;

        //Show input modal
        document.querySelector('#wifi_modal').style.display = "block";

        //Cancel button onclick 
        document.querySelector('#cancel_button').addEventListener('click', function() {
            // Hide input modal
            document.querySelector('#wifi_modal').style.display = "none";
        });

        //Connect button onclick
        document.querySelector('#connect_button').addEventListener('click', () => {
            input_password(wifi_name);
        });
        
    })
    
});
