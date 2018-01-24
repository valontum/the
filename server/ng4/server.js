const express = require('express');
const path = require('path');
const http = require('http');
const bodyParser = require('body-parser');
var cookieSession = require('cookie-session');
session = require('express-session');
multer = require('multer');
upload = multer({ dest: 'uploads/' });

// Get our API routes
const api = require('./server/routes/api');

const app = express();
app.set('trust proxy', 1);

app.use(cookieSession({
    name: 'session',
    keys: ['key1', 'key2']
}))


app.use(function (req, res, next) {

    // Website you wish to allow to connect
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:4200');

    // Request methods you wish to allow
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');

    // Request headers you wish to allow
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');

    // Set to true if you need the website to include cookies in the requests sent
    // to the API (e.g. in case you use sessions)
    res.setHeader('Access-Control-Allow-Credentials', true);

    // Pass to next layer of middleware
    next();
});
// Parsers for POST data
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Point static path to dist


// Set our api routes
app.use('/api', api);

// Catch all other routes and return the index file




/**
 * Get port from environment and store in Express.
 */
const port = process.env.PORT || '3000';
app.set('port', port);

/**
 * Create HTTP server.
 */
const server = http.createServer(app);

/**
 * Listen on provided port, on all network interfaces.
 */
server.listen(port, () => console.log(`API running on localhost:${port}`));
