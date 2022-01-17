var lan = 'ch';
var language = {
  en: {
    header: 'Sign In',
    sub_header: 'Please sign in to XiaoRong Speaker',
    create_account:
      '<a href="https://accounts.google.com/signup" class="underline" target="_blank">Create Account</a>',
  },
  ch: {
    header: '登入',
    sub_header: '登入您的小絨音箱',
    create_account:
      '還沒有帳號嗎？<a href="https://accounts.google.com/signup" class="underline" target="_blank">馬上註冊!</a>',
  },
};
const urlObj = new URL(document.URL);
let flask_base_url = urlObj.protocol + '//' + urlObj.hostname;

if (urlObj.port != undefined) {
  flask_base_url = flask_base_url.concat(':' + urlObj.port);
}

window.onload = function () {
  get_lan();
};
function post_data(access_token, name, email, client_secret) {
  fetch(flask_base_url + '/user_info', {
    method: 'POST',
    body: JSON.stringify({
      access_token: access_token,
      full_name: name,
      email: email,
      client_secret: client_secret,
      language: lan
    }),
    headers: { 'Content-Type': 'application/json' },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('Success:', data);
      // Redirect to setting.html
      window.location.href = `setting.html?lan=${lan}`;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}
var googleUser = {};
var startApp = function () {
  gapi.load('auth2', function () {
    // Retrieve the singleton for the GoogleAuth library and set up the client.
    auth2 = gapi.auth2.init({
      client_id:
        '49787076828-7u9ur75t32k9oqf557l9091jh6n9dnqi.apps.googleusercontent.com',
      cookiepolicy: 'single_host_origin',
      fetch_basic_profile: 'false',
      scope: 'profile',
      // Request scopes in addition to 'profile' and 'email'
      //scope: 'additional_scope'
    });
    attachSignin(document.getElementById('googleSignIn'));
  });
};

function attachSignin(element) {
  console.log(element.id);
  auth2.attachClickHandler(
    element,
    {},
    function (googleUser) {
      var profile = googleUser.getBasicProfile();
      let authreponse = googleUser.getAuthResponse();
      let access_token = authreponse.access_token;
      let name = profile.getName();
      let email = profile.getEmail();
      let client_secret = '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';

      //console.log(authreponse);
      //console.log(access_token);
      //console.log(profile);
      //console.log(name);
      //console.log(email);

      //window.location.href = 'setting.html';

      // POST user's ID to backend
      post_data(access_token, name, email, client_secret);
    },
    function (error) {
      //alert(JSON.stringify(error, undefined, 2));
    }
  );
}

function get_lan() {
  const params = new URLSearchParams(window.location.search);
  var trans = {};

  if (params.has('lan')) {
    lan = params.get('lan');
  }

  trans = language[lan];

  // Set language
  for (let key in trans) {
    document.getElementById(key).innerHTML = trans[key];
  }

  console.log(params.has('lan'));
}

startApp();
