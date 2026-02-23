// Polyfill for Node.js < 18.14.0
require('./metro-polyfill');

const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

module.exports = config;
