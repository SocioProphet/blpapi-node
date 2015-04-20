var c = require('./Console.js');
var blpapi = require('blpapi');

var hp = c.getHostPort();
// Add 'authenticationOptions' key to session options if necessary.
var session = new blpapi.Session({ serverHost: hp.serverHost,
                                   serverPort: hp.serverPort });

var seclist = ['AAPL US Equity', 'VOD LN Equity'];

var sublist = [
	new blpapi.Subscription(seclist[0], ['LAST_PRICE', 'BID', 'ASK']),
	new blpapi.Subscription(seclist[1], ['LAST_PRICE', 'BID', 'ASK'])
];

sublist[0].on('data', function (data) { console.log(seclist[0]); c.log(data); });
sublist[0].on('error', function (error) { console.log(seclist[0]); c.log(error); });
sublist[1].on('data', function (data) { console.log(seclist[1]); c.log(data); });
sublist[1].on('error', function (error) { console.log(seclist[1]); c.log(error); });

// Helper to put the console in raw mode and shutdown session on close
c.createConsole(session);

session.start().then(subscribe).catch(function (error) {
    c.log(error);
});

function subscribe() {
    // Subscribe to market bars for each security
    session.subscribe(sublist).then(function () {
 	    setTimeout(unsubscribe, 10000);
    }).catch(function (error) {
        console.log('Subscribe failure:', error);
    });
}

function unsubscribe() {
	session.unsubscribe(sublist);
}

// Local variables:
// c-basic-offset: 4
// tab-width: 4
// indent-tabs-mode: nil
// End:
//
// vi: set shiftwidth=4 tabstop=4 expandtab:
// :indentSize=4:tabSize=4:noTabs=true:

// ----------------------------------------------------------------------------
// Copyright (C) 2014 Bloomberg L.P.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to
// deal in the Software without restriction, including without limitation the
// rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
// sell copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
// IN THE SOFTWARE.
// ----------------------------- END-OF-FILE ----------------------------------
