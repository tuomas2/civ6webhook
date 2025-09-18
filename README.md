# Civ6 Notifier Webhook Service

This is a simple webhook service that listens for incoming POST requests and sends notifications via the PushOver API.

## Features

- Receives webhook payloads with a `message` field
- Sends push notifications to your device using PushOver
- Configurable via environment variables
- Docker support with production WSGI server (Gunicorn)
- Nginx proxy configuration sample

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Secrets File**:
   Create a file named `civ6notifier.secrets` with your PushOver credentials:
   ```
   export PUSHOVER_TOKEN=your_pushover_app_token
   export PUSHOVER_USER=your_pushover_user_key
   ```
   Get these from https://pushover.net/

3. **Run the Service**:
   ```bash
   ./run.sh
   ```
   This will source the secrets and start the Flask app on port 5000.

## Docker Usage

The Docker container uses Gunicorn as a production WSGI server with 4 worker processes for better performance and reliability.

1. **Build and Run with Script**:
   ```bash
   ./run_docker.sh
   ```
   This will source the secrets, build the image, and run the container with Gunicorn.

2. **Manual Build and Run**:
   ```bash
   docker build -t civ6notifier .
   source civ6notifier.secrets
   docker run -p 5000:5000 \
     -e PUSHOVER_TOKEN=$PUSHOVER_TOKEN \
     -e PUSHOVER_USER=$PUSHOVER_USER \
     civ6notifier
   ```

   Note: The `civ6notifier.secrets` file uses bash export syntax for compatibility with both direct Python execution and Docker.

## Nginx Configuration

To integrate with your existing server, use the provided `nginx-sample.conf` as a template. Copy it to `/etc/nginx/sites-available/` and create a symlink in `/etc/nginx/sites-enabled/`. Adjust the `server_name` and paths as needed.

Example:
```bash
sudo cp nginx-sample.conf /etc/nginx/sites-available/civ6notifier
sudo ln -s /etc/nginx/sites-available/civ6notifier /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## API Usage

Send a POST request to `http://yourserver/webhook` (or `http://localhost:5000/webhook` if running locally) with JSON payload:

```json
{
  "message": "Your notification message here"
}
```

The service will send the message as a push notification via PushOver.

## Security Notes

- Keep `civ6notifier.secrets` secure and do not commit it to version control
- Consider adding authentication to the webhook endpoint for production use
- Use HTTPS in production (configure SSL in nginx)

## Troubleshooting

If you're getting 404 errors or connection issues:

1. **Run the test script**:
   ```bash
   ./test_service.sh
   ```

2. **Check if the service is running**:
   ```bash
   docker ps | grep civ6notifier
   ```

3. **Check Docker logs**:
   ```bash
   docker logs $(docker ps -q -f name=civ6notifier)
   ```

4. **Test local access**:
   ```bash
   curl http://localhost:5000/webhook -X POST -H "Content-Type: application/json" -d '{"message":"Test"}'
   ```

5. **Check nginx configuration**:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

6. **Check nginx error logs**:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

7. **Verify firewall settings**:
   ```bash
   sudo ufw status
   ```

8. **Update deployment**:
   ```bash
   ./update.sh  # Sync files to server
   # Then on server: ./run_docker.sh
   ```

## Deployment

To deploy updates to your production server:

1. **Sync files to server**:
   ```bash
   ./update.sh
   ```

2. **On the server, rebuild and restart**:
   ```bash
   cd ~/civ6notifier
   ./run_docker.sh
   ```

The `update.sh` script uses rsync to efficiently sync only changed files to your tp2 server, excluding sensitive files and build artifacts.