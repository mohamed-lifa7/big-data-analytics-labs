# Solving Lab 4

## Step 1: Create a Docker Hub Account
Go to `https://hub.docker.com` and sign up. 
You will need your username for the next steps. 
mine is `mohamedlifa7`

## Step 2: Build the Docker Image
This command builds the image from your `Dockerfile` and tags it with the name `taxi-analysis:v1`.

```bash
docker build -t taxi-analysis:v1 .
```

## Step 3: Push the Image to Docker Hub
```bash
# 1. Log in to Docker Hub
docker login

# 2. Tag your image
docker tag taxi-analysis:v1 mohamedlifa7/taxi-analysis:v1

# 3. Push the image
docker push mohamedlifa7/taxi-analysis:v1
```

## Step 4: Pull the Image from Docker Hub
This step is just to verify. You can run this on a different computer (or run `docker rmi mohamedlifa7/taxi-analysis:v1` first to remove it) to prove it works.

```bash
docker pull mohamedlifa7/taxi-analysis:v1
```

## Step 5, 6, 7 Combined
Steps 5, 6, and 7 in the PDF are contradictory. Step 5 creates containers, but Step 7 tries to create them again with the same names, which will cause an error.

Here is a much better way that accomplishes all the goals of creating containers (Step 5), networking them (Step 6), and mapping ports (Step 7) in one clean workflow.

### A. Create the network first:
```bash
docker network create tp-network
```

### B. Run your three containers
I've combined the commands from steps 5, 6, and 7 here.

- `-d` runs the container in detached mode.
- `--name` gives it a name.
- `--net` connects it to the network you just made.
- `-p` maps the ports (even though our script doesn't use them, this fulfills the lab requirement).
- `-v` (Volume): This is the most important part. It links the /app/output folder inside the container to a new folder on your host computer. This is how you'll get the CSV files for Power BI.

```bash
docker run -d -p 8001:80 --name container1 --net tp-network -v $(pwd)/output1:/app/output mohamedlifa7/taxi-analysis:v1
docker run -d -p 8002:80 --name container2 --net tp-network -v $(pwd)/output2:/app/output mohamedlifa7/taxi-analysis:v1
docker run -d -p 8003:80 --name container3 --net tp-network -v $(pwd)/output3:/app/output mohamedlifa7/taxi-analysis:v1
```

## Step 8: Verify the Containers
Wait a few seconds for the containers to start and run the script.

### A. See running containers
Because we added sleep 3600 to the Dockerfile, the containers will stay running.
```bash
docker ps
```
You should see `container1`, `container2`, and `container3` all listed.

### B. Verify the network
This command proves you completed Step 6.

```bash
docker network inspect tp-network
```

You will see all three containers listed under the "Containers" section of the output.
