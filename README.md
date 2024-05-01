# Tradingview-Telegram-Bot

<br>
This project provides simple webhook service which can be used to send tradingview alerts to telegram along with current chart snapshot


<h4>Mandatory Environment Variables</h4>
<ul>
<li>TOKEN - Telegram Access Token</li>
<li>CHANNEL - Telegram Channel Id</li>
</ul>

<h4>Optional Environment Variables</h4>
These are only required if we are using logged in sessions for chart capture.
<ul>
<li>username - Your tradingview username</li>
<li>password - Your tradingview password</li>
<li>sessionid - Your tradingview session id. If you don't want to use userrname and password, this is an alternative. sessionid can be obtained from browser cookies</li>
</ul>


<h1>Usage</h1>
Once up and running, you will be able to use following calls 

<h3>POST /webhook/</h3>

<h4>Query Parameters</h4>
<ul>
<li> <b>jsonRequest</b> - can be set as true/false. Default is false. If set to true, the payload should be a standard json. Output to telegram will be sent in tabular format. If not set or if set to false, output to telegram will be clear text.</li>
<li> <b>tblfmt</b> - table format to be used when jsonRequest is set to true. Default is plain. The values are exactly same as the ones required for <a href="https://pypi.org/project/tabulate/">tabulate</a> package. 
<li> <b>chart</b> - Send the chart id if required to send chart snapshot along with alert message. For this to work - chart needs to be either a shared chart or environment variables for tvusername and tvpassword should be set to the user who has access to given chart.</li>
<li> <b>ticker</b> - Chart ticker. You no longer need to use different chart for different tickers. You can have a common chart and pass ticker to it so that chart will automatically switch to given ticker before taking screenshot</li>
<li> <b>delivery</b> - Taking chart snapshot takes time. This also delays the delivery of alert message. To avoid this, we can use this option - delivery=asap so that alert message will be sent as soon as possible and chart is sent later. If this parameter is not set, then both the messages will be delivered together.</li>
</ul>

