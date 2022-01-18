var lan = 'ch';
var language = {
  en: {
    header: 'Setup your XiaoRong',
    label_location: 'Location',
    location:
      '<option>Hsinchu County</option><option>Kinmen County</option><option>Miaoli County</option><option>New Taipei City</option><option>Yilan County</option><option>Yunlin County</option><option>Tainan City</option><option>Kaohsiung City</option><option>Changhua County</option><option>Taipei City</option><option>Nantou County</option><option>Penghu County</option><option>Keelung City</option><option>Taoyuan City</option><option>Hualien County</option><option>Lienchiang County</option><option>Taitung County</option><option>Chiayi City</option><option>Chiayi County</option><option>Pingtung County</option><option>Taichung City</option><option>Hsinchu City</option><option>Tokyo</option><option>Osaka</option><option>Seoul</option><option>Bangkok</option><option>Jakarta</option><option>Kuala Lumpur</option><option>Singapore</option><option>Manila</option><option>Ho Chi Minh City</option><option>Hanoi</option><option>Vladivostok</option><option>Burley</option><option>Guam</option><option>Honolulu</option><option>Wellington</option><option>Auckland</option><option>Sydney Airport</option><option>Perth</option><option>Brisbane</option><option>Shenyang</option><option>Qingdao</option><option>Beijing</option><option>Nanjing</option><option>Kaifeng</option><option>Lanzhou</option><option>Wuhan</option><option>Chongqing</option><option>Kunming</option><option>Shanghai</option><option>Nanchang</option><option>Hangzhou</option><option>Guangzhou</option><option>Fuzhou</option><option>Hong Kong</option><option>Haikou</option><option>Xi an</option><option>Melbourne</option><option>Sydney</option><option>Los Angeles</option><option>Las Vegas</option><option>San Francisco</option><option>Seattle</option><option>New York City</option><option>Washington,D.C</option><option>Chicago</option><option>Miami</option><option>Toronto</option><option>Vancouver</option><option>Montreal</option><option>Mexico City</option><option>Rio de Janeiro</option><option>Santiago</option><option>Lima</option><option>Buenos Aires</option><option>Oslo</option><option>Madrid</option><option>Copenhagen</option><option>Helsinki</option><option>Frankfurt</option><option>Berlin</option><option>Geneva</option><option>Brussels</option><option>London</option><option>Paris</option><option>Vienna</option><option>Roma</option><option>Venice</option><option>Budapest</option><option>Athens</option><option>Warsaw</option><option>Prague</option><option>Amsterdam</option><option>Stockholm</option><option>Lisbon</option><option>Cairo</option><option>Johannesburg</option><option>Kathmandu</option><option>New Dehli</option><option>Istabul</option><option>Moscow</option>',
    label_timezone: 'Timezone',
    label_speaker_name: 'Name',
    next_button: 'Next',
  },
  ch: {
    header: '設定您的小絨',
    label_location: '城市',
    location:
      '<option>新竹縣</option><option>金門縣</option><option>苗栗縣</option><option>新北市</option><option>宜蘭線</option><option>雲林縣</option><option>台南市</option><option>高雄市</option><option>彰化縣</option><option>臺北市</option><option>南投縣</option><option>澎湖縣</option><option>基隆市</option><option>桃園市</option><option>花蓮縣</option><option>連江縣</option><option>臺東縣</option><option>嘉義市</option><option>嘉義縣</option><option>屏東縣</option><option>臺中市</option><option>新竹市</option><option>東京</option><option>大阪</option><option>首爾</option><option>曼谷</option><option>雅加達</option><option>吉隆坡</option><option>新加坡</option><option>馬尼拉</option><option>胡志明市</option><option>河內</option><option>海參威</option><option>伯力</option><option>關島</option><option>檀香山</option><option>威靈頓</option><option>奧克蘭</option><option>雪梨機場</option><option>伯斯</option><option>布里斯班</option><option>瀋陽</option><option>青島</option><option>北京</option><option>南京</option><option>開封</option><option>蘭州</option><option>武漢</option><option>重慶</option><option>昆明</option><option>上海</option><option>南昌</option><option>杭州</option><option>廣州</option><option>福州</option><option>香港</option><option>海口</option><option>西安</option><option>墨爾本</option><option>雪梨</option><option>洛杉磯</option><option>拉斯維加斯</option><option>舊金山</option><option>西雅圖</option><option>紐約</option><option>華盛頓</option><option>芝加哥</option><option>邁阿密</option><option>多倫多</option><option>溫哥華</option><option蒙特婁</option><option>墨西哥城</option><option>里約</option><option>聖地牙哥</option><option>利馬</option><option>布宜諾利艾利斯</option><option>奧斯陸</option><option>馬德里</option><option>哥本哈根</option><option>赫爾辛基</option><option>法蘭克福</option><option>柏林</option><option>日內瓦</option><option>布魯塞爾</option><option>倫敦</option><option>巴黎</option><option>維也納</option><option>羅馬</option><option>威尼斯</option><option>布達佩斯</option><option>雅典</option><option>華沙</option><option>布拉格</option><option>阿姆斯特丹</option><option>斯德哥爾摩</option><option>里斯本</option><option>開羅</option><option>約翰尼斯堡</option><option>加德滿都</option><option>新德里</option><option>伊斯坦布爾</option><option>莫斯科</option>',
    label_timezone: '時區',
    label_speaker_name: '名稱',
    next_button: '下一步',
  },
};
window.onload = function () {
  get_lan();
};
const urlObj = new URL(document.URL);
let flask_base_url = urlObj.protocol + '//' + urlObj.hostname;

if (urlObj.port != undefined) {
  flask_base_url = flask_base_url.concat(':' + urlObj.port);
}

function get_lan() {
  const params = new URLSearchParams(window.location.search);
  var trans = {};

  if (params.has('lan')) {
    lan = params.get('lan');
  }
  trans = language[lan];

  if (lan == 'en') {
    // Update placeholder of input form
    document.getElementById('speaker_name').placeholder = 'XiaoRong speaker';
  } else if (lan == 'ch') {
    // Update placeholder of input form
    document.getElementById('speaker_name').placeholder = '小絨音箱';
  }

  // Set language
  for (let key in trans) {
    document.getElementById(key).innerHTML = trans[key];
  }

  console.log(params.has('lan'));
}
//get_lan();
function post_info(location, time, speaker_name) {
  fetch(flask_base_url + '/speaker_info', {
    method: 'POST',
    body: JSON.stringify({
      location: location,
      time: time,
      speaker_name: speaker_name,
      language: lan
    }),
    headers: { 'Content-Type': 'application/json' },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('Success:', data);
      window.location.href = `done.html?lan=${lan}`;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

document.querySelector('button').addEventListener('click', () => {
  //get speaker's name
  var speaker_name = document.querySelector('#speaker_name').value;

  // check if speaker_name contains all white spaces
  var all_white_spaces = true;
  for (let i = 0; i < speaker_name.length; i++) {
    if (speaker_name[i] != ' ') {
      all_white_spaces = false;
      break;
    }
  }
  if (speaker_name == '' || all_white_spaces) {
    speaker_name = document.getElementById('speaker_name').placeholder;
  }

  // get location
  var location = document.querySelector('#location').value;

  var time = document.querySelector('#time').value;


  //post info to API
  post_info(location, time, speaker_name);
});
