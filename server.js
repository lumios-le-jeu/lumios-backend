const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

let clients = [];

wss.on('connection', (ws) => {
  console.log("Un joueur s'est connecté.");

  // Ajouter le client à la liste des clients
  clients.push(ws);

  ws.on('message', (message) => {
    console.log("Message reçu du client :", message);

    // Diffuser le message à tous les clients sous forme de JSON
    clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(typeof message === 'string' ? message : JSON.stringify(message));
      }
    });
  });

  ws.on('close', () => {
    console.log("Un joueur s'est déconnecté.");
    clients = clients.filter((client) => client !== ws);
  });
});

server.listen(3001, () => {
  console.log('Serveur WebSocket en écoute sur le port 3001');
});
