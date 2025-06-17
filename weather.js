#!/usr/bin/env node
// Simple Node.js script to fetch current weather for a city using Open-Meteo
// Demonstrates using a different language to access the same API.

const https = require('https');

function getJson(url) {
  return new Promise((resolve, reject) => {
    https.get(url, {headers: {'User-Agent': 'weather-app-node'}}, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (err) {
          reject(err);
        }
      });
    }).on('error', reject);
  });
}

async function getLatLon(city) {
  const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(city)}&format=json&limit=1`;
  const data = await getJson(url);
  if (data && data.length > 0) {
    return {lat: data[0].lat, lon: data[0].lon};
  }
  throw new Error('City not found');
}

async function getWeather(city) {
  const {lat, lon} = await getLatLon(city);
  const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`;
  const data = await getJson(url);
  data.city = city;
  return data;
}

async function main() {
  const city = process.argv.slice(2).join(' ');
  if (!city) {
    console.log('Usage: node weather.js <city>');
    process.exit(1);
  }
  try {
    const weather = await getWeather(city);
    if (weather.current_weather) {
      console.log(`Weather in ${weather.city}:`);
      console.log(`Temperature: ${weather.current_weather.temperature}°C`);
      console.log(`Wind: ${weather.current_weather.windspeed} km/h`);
    }
  } catch (err) {
    console.error('Error:', err.message);
  }
}

main();
