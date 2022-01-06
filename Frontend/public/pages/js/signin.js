var lan = 'ch';
var language = {
  "en":{
        'header':'Sign In',
        'sub_header': 'Please sign in to XiaoRong Speaker',
        'create_account': '<a href="https://accounts.google.com/signup" class="underline" target="_blank">Create Account</a>'
  },
  "ch":{
        'header':'登入',
        'sub_header': '登入您的小絨音箱',
        'create_account': '還沒有帳號嗎？<a href="https://accounts.google.com/signup" class="underline" target="_blank">馬上註冊!</a>'
  },
}
window.onload = function(){
  get_lan();
}
function post_id(google_id)
{
  fetch('http://localhost:3000/user_info', {
    method: 'POST',
    body: JSON.stringify({
      user_id: google_id,
    }),
    headers: {'Content-Type': 'application/json'}
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);

  })
  .catch((error) => {
    console.error('Error:', error);
  });
}
var googleUser = {};
var startApp = function() {
  gapi.load('auth2', function(){
    // Retrieve the singleton for the GoogleAuth library and set up the client.
    auth2 = gapi.auth2.init({
      client_id: "49787076828-7u9ur75t32k9oqf557l9091jh6n9dnqi.apps.googleusercontent.com",
      cookiepolicy: 'single_host_origin',
      // Request scopes in addition to 'profile' and 'email'
      //scope: 'additional_scope'
    });
    attachSignin(document.getElementById('googleSignIn'));
  });
};

function attachSignin(element) {
  console.log(element.id);
  auth2.attachClickHandler(element, {},
      function(googleUser) {
        var profile = googleUser.getBasicProfile();
        console.log(profile)
        
        // POST user's ID to backend 
        post_id(profile.getId());

        // Redirect to setting.html
          
        window.location.href = `setting.html?lan=${lan}`;
        
      }, function(error) {
        alert(JSON.stringify(error, undefined, 2));
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
    
    trans = language[lan];
   
    // Set language
    for(let key in trans)
    {
        document.getElementById(key).innerHTML = trans[key];
    }

    console.log(params.has('lan'));

}


startApp();
