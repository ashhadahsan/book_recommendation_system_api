var axios = require('axios');
var data = JSON.stringify({
  "n": 10
});

var config = {
  method: 'get',
  url: 'https://book-rec.herokuapp.com/api/books/featured',
  headers: { 
    'Content-Type': 'application/json'
  },
  data : data
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});
