Great! Let’s set up **SSL with a self-signed certificate** using **Option 2** — perfect for development or testing environments like `myapp.local` or `localhost`.

---

## 🔐 Self-Signed SSL Setup with Nginx (Step-by-Step)

---

### 🧾 STEP 1: Generate a Self-Signed SSL Certificate

Run this in your terminal:

```bash
sudo mkdir -p /etc/ssl/myapp

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout /etc/ssl/myapp/myapp.key \
-out /etc/ssl/myapp/myapp.crt \
-subj "/C=IN/ST=State/L=City/O=MyOrg/OU=IT/CN=myapp.local"
```

This will:

* Create a new SSL certificate valid for 1 year
* Save it to `/etc/ssl/myapp/myapp.crt`
* Save the private key to `/etc/ssl/myapp/myapp.key`

---

### 📝 STEP 2: Update Nginx Configuration

Edit your Nginx site file:

```bash
sudo nano /etc/nginx/sites-available/myapp
```

Replace or update the file to include **both HTTP and HTTPS blocks**:

```nginx
# HTTP block (optional - redirect to HTTPS)
server {
    listen 80;
    server_name myapp.local;

    return 301 https://$host$request_uri;
}

# HTTPS block
server {
    listen 443 ssl;
    server_name myapp.local;

    ssl_certificate     /etc/ssl/myapp/myapp.crt;
    ssl_certificate_key /etc/ssl/myapp/myapp.key;

    root /var/www/myapp/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### 🔍 STEP 3: Test and Reload Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

If no errors, Nginx has successfully applied your SSL setup.

---

### 🧪 STEP 4: Access Your Site

Open your browser and visit:

```
https://myapp.local
```

> ❗ **Important**: Since this is a self-signed certificate, your browser will show a **warning**. Click:

* **"Advanced"**
* **"Proceed to myapp.local (unsafe)"**

This is expected and safe for development.

---

### 🧠 OPTIONAL: Add Domain to `/etc/hosts`

If you're using `myapp.local`, make sure your OS resolves it locally:

```bash
sudo nano /etc/hosts
```

Add this line:

```
127.0.0.1 myapp.local
```

Now, `myapp.local` will point to your local machine.

---

## ✅ Summary

| Step                 | Command                                        |
| -------------------- | ---------------------------------------------- |
| Generate certificate | `openssl req -x509 ...`                        |
| Nginx config         | Add SSL block for `443`                        |
| Test and reload      | `sudo nginx -t && sudo systemctl reload nginx` |
| View site            | `https://myapp.local` (accept warning)         |

---

Let me know if you'd like to:

* Use **self-signed certs for multiple subdomains**
* Set up **HTTPS locally with trusted root CA** (for no browser warning)
* Add **React/Vue frontend with SSL**
* Or even **use Docker for this setup**

I'm ready!
