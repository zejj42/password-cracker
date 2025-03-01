# Password Cracker

## This project demonstrates a distributed password-cracking service built with Python and Docker. It consists of:

A **coordinator** that manages incoming CSV files containing MD5 hashes and distributes the work.
Multiple **agent** containers that each process a portion of the phone-number search space to find the matching password.
## Running the Project

# Clone This Repository

```bash
git clone https://github.com/zejj42/password-cracker
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

* Runs 1 coordinator container on port 8000.
* Runs 4 agent containers (from the same agent image) on the **Docker network**.
* Runs a Redis container on port 6379.

## Sample CSV Files

Inside the root directory, you'll find a folder named csv examples containing sample CSV files (e.g., single_hash.csv, phone_hashes.csv) you can use to test the system.

## Making a Request with Postman

Open Postman and create a new POST request to:

```bash
http://localhost:8000/uploads/
```

Attach a File under the “Body” tab, using either form-data or binary upload:

Key: file
Value: (Select a CSV file from the csv examples folder)
Send the Request. You should receive a response indicating that the tasks have been scheduled.

The coordinator will distribute the work among the agents to crack each hash. Check the logs (using either docker desktop or the following command):
```bash
docker compose logs coordinator
```

### Output

The coordinator writes output to /app/output inside the container, which is mapped to your Desktop.
To stop all services, run:

```bash
docker compose down
```
