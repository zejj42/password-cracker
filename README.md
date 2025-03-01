# Password Cracker

## This project demonstrates a distributed password-cracking service built with Python and Docker. It consists of:

A **coordinator** that manages incoming CSV files containing MD5 hashes and distributes the work.
Multiple **agent** containers that each process a portion of the phone-number search space to find the matching password.
hash hash Running the Project

#Clone This Repository

```bash
git clone <repo_url>
cd password_cracker
```

Build the Images

```bash
docker compose build
```

This creates two images: coordinator and agent.

Spin Up the Containers

```bash
docker compose up --scale agent=4 -d
```

Runs 1 coordinator container on port 8000.
Runs 4 agent containers (from the same agent image) on the Docker network.
Runs a Redis container on port 6379.
Verify Services

The coordinator is available at http://localhost:8000.
The coordinator communicates with agents using URLs like http://agent:8008 on the Docker network.
Redis is used for storing progress.
hash hash Sample CSV Files

Inside the root directory, you'll find a folder named csv examples containing sample CSV files (e.g., single_hash.csv, phone_hashes.csv) you can use to test the system.

hash hash Making a Request with Postman

Open Postman and create a new POST request to:

```bash
http://localhost:8000/uploads/
```

Attach a File under the “Body” tab, using either form-data or binary upload:

Key: file
Value: (Select a CSV file from the csv examples folder)
Send the Request. You should receive a response indicating that the tasks have been scheduled.

The coordinator will distribute the work among the agents to crack each hash. Check the logs (e.g., using docker compose logs coordinator) for progress details. If you've mapped a volume (e.g., ${HOME}/Desktop:/app/output), the generated output CSV file will appear on your Desktop.

hash hash Additional Notes

The coordinator writes output to /app/output inside the container, which is mapped to your Desktop.
To stop all services, run:

```bash
docker compose down
```
