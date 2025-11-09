const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const path = require('path');

const app = express();

// Servir archivos estáticos
app.use(express.static(path.join(__dirname, 'public')));

// Proxy para API
app.use('/api', createProxyMiddleware({
    target: 'http://backend:5000',
    changeOrigin: true,
    pathRewrite: { '^/api': '' },
    onError: (err, req, res) => {
        console.error('Proxy error:', err);
        res.status(500).json({ error: 'Proxy error: ' + err.message });
    }
}));

app.listen(3000, () => {
    console.log(' Web server running on port 3000');
    console.log(' Backend proxy at http://backend:5000');
});
