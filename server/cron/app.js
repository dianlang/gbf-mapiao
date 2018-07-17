// const cheerio = require("cheerio");
const path = require("path");
const fs = require("fs");
const request = require("request");

const config = JSON.parse(fs.readFileSync("config.json"));
var cookie = config.cookie[0];

function getJsonString() {
  let cookieString = `t=${cookie.t}; access_gbtk=${cookie.access_gbtk}; wing=${cookie.wing}; midship=${cookie.midship}`;

  let options = {
    url: `http://game.granbluefantasy.jp/teamraid${config.session}/bookmaker/content/top/`,
    headers: {
      Host: "game.granbluefantasy.jp",
      "Proxy-Connection": "keep-alive",
      "Upgrade-Insecure-Requests": 1,
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
      Accept: "application/json",
      "Accept-Encoding": "deflate",
      "Accept-Language": "zh-CN,zh;q=0.9",
      Cookie: cookieString
    },
    encoding: "utf-8"
  };
  console.log(options);
  let jsonString;
  let responseHeaders;
  request(options, function (error, response, body) {
    if (!error && response.statusCode === 200) {
      jsonString = body;
      console.log(jsonString);
    }
  });
  return jsonString;
}

console.log(getJsonString());