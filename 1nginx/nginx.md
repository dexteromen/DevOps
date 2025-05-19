Excellent — now that the Nginx errors are resolved and it’s running, let’s start fresh and **implement a custom Nginx configuration from scratch** like a pro.

---

## ✅ Goal

You’ll build a full Nginx setup with:

* A **custom domain** (`myapp.local`)
* A static **HTML site** (or later proxy to a backend)
* HTTPS (self-signed)
* Gzip & caching
* Reverse proxy (optional)

This is a clean, production-style layout you can build on.

---

## 🛠️ Step 1: Project Structure

We’ll keep everything tidy under `/var/www`.

```bash
sudo mkdir -p /var/www/myapp/html
sudo chown -R $USER:$USER /var/www/myapp/html
```

Create a simple `index.html`:

```bash
echo "<h1>Hello from MyApp</h1>" > /var/www/myapp/html/index.html
```

---

## 📄 Step 2: Create a New Site Configuration

Create a config file for `myapp`:

```bash
sudo nano /etc/nginx/sites-available/myapp
```

Paste this minimal server block:

```nginx
server {
    listen 80;
    server_name myapp.local;

    root /var/www/myapp/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
```

Disable default site (optional):

```bash
sudo rm /etc/nginx/sites-enabled/default
```

---

## 🧪 Step 3: Simulate Domain in `/etc/hosts`

Edit `/etc/hosts`:

```bash
sudo nano /etc/hosts
```

Add:

```
127.0.0.1 myapp.local
```

Save and exit.

Now try visiting `http://myapp.local` in a browser — you should see your site 🎉

---

## 🔐 Step 4: Add HTTPS (Self-Signed for Dev)

Generate cert & key:

```bash
sudo openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout /etc/ssl/private/myapp.key \
-out /etc/ssl/certs/myapp.crt
```

Now update `myapp` config to include SSL:

```nginx
server {
    listen 443 ssl;
    server_name myapp.local;

    ssl_certificate /etc/ssl/certs/myapp.crt;
    ssl_certificate_key /etc/ssl/private/myapp.key;

    root /var/www/myapp/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 80;
    server_name myapp.local;
    return 301 https://$host$request_uri;
}
```

Then:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Visit: `https://myapp.local` (accept browser warning)

---

## 🧰 Step 5: Performance & Security Tweaks

### Gzip Compression

Edit `nginx.conf` (usually `/etc/nginx/nginx.conf`) inside the `http` block:

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

### Browser Caching

In your server block:

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 30d;
    access_log off;
}
```

### Limit Upload Size

```nginx
client_max_body_size 5M;
```

---

## 🔁 Step 6: Reverse Proxy to a Backend (Optional)

Let’s say your backend runs on `http://localhost:5000`.

Change the location block:

```nginx
location / {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

> Useful for Flask, Express, Django, etc.

---

## 🧪 Step 7: Test Everything

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Then test:

* `http://myapp.local` redirects to HTTPS
* `https://myapp.local` shows site
* Gzip and caching (use browser DevTools > Network tab)

---

## 🚀 Done!

You’ve built a complete, custom Nginx site with:

✅ Static file serving
✅ HTTPS + redirect
✅ Caching + compression
✅ (Optional) Reverse proxy backend

---

### ➕ Want more?

Would you like to:

* Deploy this using **Docker**?
* Add **basic authentication** or **rate limiting**?
* Set up **multiple domains/sites**?
* Use **Let’s Encrypt for real HTTPS**?

Tell me your next goal, and I’ll guide you.
