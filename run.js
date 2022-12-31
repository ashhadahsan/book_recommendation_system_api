var axios = require("axios").default;

var options = {
  method: 'GET',
  url: 'https://book-rec.herokuapp.com/books/top',
  headers: {
    Accept: '*/*',
    'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
    'Content-Type': 'application/json'
  },
  data: {n: 10}
};

axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});