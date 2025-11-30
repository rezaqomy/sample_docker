**Update package lists**

```bash
sudo apt update
```

**Install Docker from Ubuntu repositories**

```bash
sudo apt install docker.io
```

**Add current user to the Docker group**

```bash
sudo usermod -aG docker $USER
```

**Apply new group membership without logout**

```bash
newgrp docker
```

**Run a test Docker container to verify installation**

```bash
docker run hello-world
```

**Download the latest Ubuntu image from Docker Hub**

```bash
docker pull ubuntu:latest
```

**List all Docker images stored locally**

```bash
docker image ls # or docker images
```

**Run an interactive Ubuntu container with a bash shell**

```bash
docker run -it ubuntu /bin/bash
```

**List currently running containers**

```bash
docker ps # or docker container ls
```

**List all containers, including stopped ones**

```bash
docker ps -a # or docker container ls -a
```

**Stop a running container**

```bash
docker stop container_name
```

**Start a stopped container and attach to it interactively**

```bash
docker start -ai container_name
```

**Remove a Docker container**

```bash
docker container rm container_name
```

**Install LazyDocker using Alpine package manager**

```bash
apk add lazydocker
```

**Run Uptime Kuma monitoring tool**

```bash
docker run -d -p 3001:3001 louislam/uptime-kuma
```

**Run Mattermost preview server**

```bash
docker run -d --name mattermost -p 8065:8065 mattermost/mattermost-preview
```

**Run Portainer for Docker management**

```bash
docker run -d -p 9000:9000 \
 -v /var/run/docker.sock:/var/run/docker.sock \
  portainer/portainer-ce
```

**Docker Compose file for WordPress + MySQL**

```yaml
version: '3.8'

services:
  wordpress:
    image: wordpress:latest
    container_name: wordpress
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    depends_on:
      - db

  db:
    image: mysql:5.7
    container_name: wordpress-db
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

**Docker Compose file for Jellyfin, qBittorrent, Prowlarr, Radarr**

```yaml
version: "3.8"

services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    ports:
      - "8096:8096"
    volumes:
      - ./config/jellyfin:/config
      - ./media:/media
    restart: unless-stopped

  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      - WEBUI_PORT=8080
      - QBT_USERNAME=admin
      - QBT_PASSWORD=admin
    ports:
      - "8080:8080"
      - "6881:6881"
      - "6881:6881/udp"
    volumes:
      - ./config/qbittorrent:/config
      - ./downloads:/downloads
    restart: unless-stopped

  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    ports:
      - "9696:9696"
    volumes:
      - ./config/prowlarr:/config
    restart: unless-stopped

  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    ports:
      - "7878:7878"
    volumes:
      - ./config/radarr:/config
      - ./media/movies:/movies
      - ./downloads:/downloads
    restart: unless-stopped

volumes:
  jellyfin_config:
  downloads:
  media:
```

**Clone a sample Docker project from GitHub**

```bash
git clone https://github.com/rezaqomy/sample_docker.git
```
