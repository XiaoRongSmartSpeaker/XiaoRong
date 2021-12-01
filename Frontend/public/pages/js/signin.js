function post_id(google_id)
{
  fetch('API', {
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
      client_id: "794994058097-jp4imiqashiui62cdp8e0liahs4grfcp.apps.googleusercontent.com",
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
          
        window.location.href = "setting.html";
        
      }, function(error) {
        alert(JSON.stringify(error, undefined, 2));
      });
}
startApp();
