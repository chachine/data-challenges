[//]: # ( challenge tech stack: fastapi uvicorn )

[//]: # ( challenge instructions )

## Objective

Use **FastAPI** in order to create an API for your model.

Run that API on your machine. Then put it in production.

## Context

Now that we have a performant model trained in the cloud, we will expose it to the world 🌍

We will create a **Prediction API** for our model, run it on our machine in order to make sure that everything works correctly. Then we will deploy it in the cloud so that everyone can play with our model!

In order to do so, we will:
- Challenge 1 : create a **Prediction API** using **FastAPI**
- Challenge 2 : create a **Docker image** containing the environment required in order to run the code of our API
- Challenge 3 : push this image to **Google Cloud Run** so that it is instantiated as a **Docker container** that will run our code and allow developers all over the world to use it

# 1️⃣ PROJECT SETUP 🛠

<details>
  <summary markdown='span'><strong>❓ Instructions </strong></summary>

## Environment

Copy your `.env` file from the previous package version:

```bash
cp ~/<user.github_nickname>/{{local_path_to('07-ML-Ops/03-Automate-model-lifecycle/01-Automate-model-lifecycle')}}/.env .env
```

OR

Use the `env.sample` provided, replacing the environment variable values by yours.

## API directory

A new `taxifare/api` directory has been added to the project to contain the code of the API along with 2 new configuration files within the challenge project directory:

```bash
.
├── Dockerfile          # 🎁  NEW Building instructions
├── MANIFEST.in         # 🎁  NEW Config file for production purpose
├── Makefile            # Good old task manager
├── README.md
├── requirements.txt    # All the dependencies you need to run the package
├── setup.py            # Package installer
├── taxifare
│   ├── api             # 🎁  NEW API directory
│   │   ├── __init__.py
│   │   └── fast.py     # 🎁  NEW Where the API lays
│   ├── data_sources    # Data stuff
│   ├── flow            # DAG stuff
│   ├── interface       # Package entry point
│   └── ml_logic        # ML stuff
└── tests
```

Now, have a look at the `requirements.txt`. You can see new comers:

``` bash
# API
fastapi         # API framework
pytz            # Timezones management
uvicorn         # Web server
# tests
httpx           # HTTP client
pytest-asyncio  # Asynchronous I/O support for pytest
```

⚠️ Make sure perform a **clean install** of the package.

<details>
  <summary markdown='span'>❓ How?</summary>

`make reinstall_package` of course 😉

</details>

## Running the API with FastAPI and a Uvicorn server

We provide you with with a FastAPI skeleton in the `fast.py` file.

**💻 Launch the API**

<details>
  <summary markdown='span'>💡 Hint</summary>

You probably need a `uvicorn` web server..., with a 🔥 reloading...

In case you can't find the proper syntax, keep calm and look at your `Makefile`, we provided you with a new task `run_api`.

If you run into an error `Address already in use`, the port `8000` on your local machine might already be used by another application.

You can check this by running `lsof -i :8000`. If the command returns something, then the port `8000` is already in use.

In this case specify another port in the [0, 65535] range in the `run_api` command using the `--port` parameter.
</details>

**❓ How do you consult your running API?**

<details>
  <summary markdown='span'>Answer</summary>

💡 Your API is available on a local port, `8000` probably 👉 [http://localhost:8000](http://localhost:8000).
Go visit it!

</details>

You have probably not seen much.

**❓ Which endpoints are available?**

<details>
  <summary markdown='span'>Answer</summary>

There is only one endpoint _partially_ implemented at the moment, the root endpoint `/`.
The unimplemented root page is a little raw, remember you can always find more info on the API using the swagger endpoint 👉 [http://localhost:8000/docs](http://localhost:8000/docs)

</details>

</details>

<br>

# 2️⃣  Build the API 📡

<details>
  <summary markdown='span'><strong>❓ Instructions </strong></summary>
An API is defined by its specifications. E.g. [GitHub repositories API](https://docs.github.com/en/rest/repos/repos). You will find below the API specifications you need to implement.

## Specifications

### Root

- GET `/`
- Response
Status: 200
```json
{
    'greeting': 'Hello'
}
```

**💻 Implement the Root endpoint `/`**

**👀 Look at your browser 👉 [http://localhost:8000](http://localhost:8000)**

**🐛 Inspect the server logs and add some `breakpoint()` to debug**

Once and _only once_ your API responds as required:
**🧪 Test your implementation with `make test_api_root`**

**🚀 Commit and push your code!**

### Prediction

- GET `/predict`
- Query parameters

| Name | Type | Sample |
|---|---|---|
| pickup_datetime | DateTime |  `2013-07-06 17:18:00` |
| pickup_longitude | float |  `-73.950655` |
| pickup_latitude | float |  `40.783282` |
| dropoff_longitude | float |  `-73.950655` |
| dropoff_latitude | float |  `40.783282` |
| passenger_count | int |  `2` |

- Response `Status 200`
- Code sample
```bash
GET http://localhost:8000/predict?pickup_datetime=2013-07-06 17:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2
```
Example response:
```json
{
    'fare_amount': 5.93
}
```

**❓ How would you proceed to implement the `/predict` endpoint? 💬 Discuss with your buddy.**


<details>
  <summary markdown='span'>💡 Hints</summary>

Ask yourselves the following questions:
- How should we handle the query parameters?
- How can we re-use the `taxifare` model package in the most lightweight way ?
- How should we build `X_pred`? What does it look like?
- How to render the correct response?
</details>

<details>
  <summary markdown='span'>⚙️ Configuration</summary>

Have you put a trained model in _Production_ in MLflow? If not, you can use the following configuration, which already has a saved model:

    ``` bash
    MODEL_TARGET=mlflow
    MLFLOW_TRACKING_URI=https://mlflow.lewagon.ai
    MLFLOW_EXPERIMENT=taxifare_experiment_krokrob
    MLFLOW_MODEL_NAME=taxifare_krokrob
    ```

</details>

<details>
  <summary markdown='span'>🍔 Food for thought</summary>

1. Investigate the data types of the query parameters, you may need to convert them into the types the model requires.
2. It's more convenient to re-use the methods available in the `taxifare/ml_logic` package rather than the main routes in `taxifare/interface`. Always load the minimal amount of code!
3. In order to make a prediction with the trained model, you must provide a valid `X_pred` but the `key` is missing!
4. FastAPI can only render data type from the [Python Standard Library](https://docs.python.org/3.8/library/stdtypes.html), you may need to convert `y_pred` to match this requirement

</details>

**👀 Inspect your browser response 👉 [http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2](http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2)**

**👀 Inspect the server logs while you query the endpoint**

Once and _only once_ your API responds as required:
**🧪 Test your implementation with `make test_api_predict`**

👏 Congrats, you build your first ML predictive API!


### ⚡️ Faster predictions

Did you notice your prediction were a bit slow? Why?

The answer is in visible in your logs!

We want to avoid loading the heavy deep-learning model from MLflow at each GET request! The trick is to load the model in memory at app startup and store it in a global variable in `app.state`, which is kept in memory and accessible across all routes instantly!

This will prove very usefull for demo days!

<details>
  <summary markdown='span'>⚡️ like this ⚡️ </summary>

```python
app = FastAPI()
app.state.model = ...

@app.get("/predict")
...
app.state.model.predict(...)
```

</details>



</details>

<br>

# 3️⃣ Build a Docker image for our API 🐳

<details>
  <summary markdown='span'><strong>❓ Instructions </strong></summary>

We now have a working **predictive API** which can be queried from our local machine.

We want to make it available to the world. In order to do that, the first step is to create a **Docker image** that contains the environment required to run the API and make it run _locally_ on Docker.

**❓ What are the 3 steps to run the API on Docker?**

<details>
  <summary markdown='span'>Answer</summary>

1. **Create** a `Dockerfile` containing the the instructions to build the API
1. **Build** the image locally on Docker
1. **Run** the API on Docker locally to check it is responding as required

</details>

## Setup

You need Docker daemon to run on your machine so you  will be able to build and run the image locally.

**💻 Launch Docker daemon**

<details>
  <summary markdown='span'>MacOSX</summary>

Launch the Docker Desktop app, you should see a whale in your menu bar.

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/macos-docker-desktop-running.png" target="_blank"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/macos-docker-desktop-running.png" width="150" alt="verify that Docker Desktop is running"></a>

</details>

<details>
  <summary markdown='span'>Windows WSL2 & Ubuntu</summary>

Launch the Docker app.

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/windows-docker-app.png" target="_blank"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/windows-docker-app.png" width="150" alt="verify that Docker Desktop is running"></a>

</details>

**✅ Check Docker daemon is up and running with `docker info` in your terminal**

A nice stack of logs should print:
<a href="https://github.com/lewagon/data-setup/raw/master/images/docker_info.png" target="_blank"><img src='https://github.com/lewagon/data-setup/raw/master/images/docker_info.png' width=150></a>


## `Dockerfile`

As a reminder, here is the project directory structure:

```bash
.
├── Dockerfile          # 👉 Building instructions
├── MANIFEST.in         # 🆕 Config file for production purpose
├── Makefile            # Good old task manager
├── README.md           # Package documentation
├── requirements.txt    # All the dependencies you need to run the package
├── setup.py            # Package installer
├── taxifare
│   ├── api             # ✅ API directory
│   │   ├── __init__.py
│   │   └── fast.py     # ✅ Where the API lays
│   ├── data_sources    # Data stuff
│   ├── flow            # DAG stuff
│   ├── interface       # Package entry point
│   └── ml_logic        # ML logic
└── tests               # Your favorite 🍔
```

**❓ What are the key ingredients a `Dockerfile` needs to cook a delicious Docker image?**

<details>
  <summary markdown='span'>Answer</summary>

Here the most common instructions of good `Dockerfile`:
- `FROM`: select a base image for our image (the environment in which we will run our code), this is usually the first instruction
- `COPY`: copy files and directories inside of our image (our package and the associated files for example)
- `RUN`: execute a command **inside** of the image being built (for example, install the package dependencies)
- `CMD`: execute the **main** command that will be executed when we run our **Docker image**. There can be only one `CMD` instruction inside of a `Dockerfile`. It is usually the last instruction

</details>

**❓ What should the base image contain to build our image on top of it?**

<details>
  <summary markdown='span'>💡 Hints</summary>

You can start from a raw linux (Ubuntu) image, but then you'll have to install python, and pip, before installing taxifare!

OR

You can choose an image with Python (and pip) already installed ! (recommended) ✅

</details>

**💻 Write the instructions needed to build the API image in the `Dockerfile` with the following specifications:**

- ✅ it should contain the same Python version of your virtual env
- ✅ it should contain the necessary directories from the `/taxifare` directory to allow the API to run
- ✅ it should contain the dependencies list
- ✅ the API depencies should be installed
- ✅ the web server should be launched when the container is started from the image
- ✅ the web server should listen to the HTTP requests coming from outside the container (cf `host` parameter)
- ✅ the web server should be able listen to a specific port defined by an environment variable `$PORT` (cf `port` parameter)

<details>
  <summary markdown='span'>⚡️ Kickstart pack</summary>

Here is the skeleton of the `Dockerfile`:

  ```Dockerfile
  FROM image
  COPY taxifare
  COPY dependencies
  RUN install dependencies
  CMD launch API web server
  ```

</details>

<details>
  <summary markdown='span'><strong>🚨 Apple Silicon users</strong>, expand me and read carefully</summary>

You will not be able to test your container locally with the tensorflow package since the current version does not install properly on _Apple Silicon_ machines.

The solution is to use one image to test your code locally and another one to push your code to production.

👉 Refer to the commands in the `Dockerfile_silicon` file in order to build and test your **local image** and build and deploy to production your **production image**
</details>



**❓ How would you check if the `Dockerfile` instructions will execute what you wanted?**

<details>
  <summary markdown='span'>Answer</summary>

You can't at this point! 😁 You need to build the image and check if it contains everything required to run the API. Go to the next section: Build the API image.
</details>

## Build the API image

Now is the time to **build** the API image on Docker so you can check if it satisfies the requirements and be able to run it on Docker.

**❓ How do you build an image with Docker?**

<details>
  <summary markdown='span'>⚙️ Configuration</summary>

You may add a variable to your project configuration for the docker image name. You will be able to reuse it in the `docker` commands:

``` bash
IMAGE=image-name
```
</details>

<details>
  <summary markdown='span'>Answer</summary>

Make sure you are in the directory of the `Dockefile` then:

```bash
docker build --tag=$IMAGE .
```
</details>

**💻 Choose a meaningful name for the API image then build it**

Once built, the image should be visible in the list of images built with the following command:

``` bash
docker images
```

<img src='https://wagon-public-datasets.s3.amazonaws.com/data-science-images/07-ML-OPS/docker_images.png'>

**🕵️‍♀️ The image you are looking for does not appear in the list? Ask for help 🙋‍♂️**

## Check the API image

Now the image is built let's check it satisfies the specifications to run the predictive API. Docker comes with a handy command to **interactively** communicate with the shell of the image:

``` bash
docker run -it -e PORT=8000 -p 8000:8000 $IMAGE sh
```

<details>
  <summary markdown='span'>🤖 Decrypt</summary>

- `docker run $IMAGE` run the image
- `-it` enable the interactive mode
- `-e PORT=8000` specify the environment variable `$PORT` the image should listen to
- `sh` launch a shell console
</details>

A shell console should open, you are inside the image 👏.

**💻 Check the image is correctly set up:**

- ✅ The python version is the same as your virtual env
- ✅ Presence of the `/taxifare` directory
- ✅ Presence of the `requirements.txt`
- ✅ The dependencies are all installed

<details>
  <summary markdown='span'>🙈 Solution</summary>

- `python --version` to check the Python version
- `ls` to check the presence of the files and directories
- `pip list` to check the requirements are installed
</details>

Exit the terminal and stop the container at any moment with:

``` bash
exit
```

**✅ ❌ All good? If something is missing, you  would probably need to fix your `Dockerfile` and re-build the image again**

## Run the API image

In the previous section you learned how to interact with the image shell. Now is the time to run the predictive API image and
test if the API responds as it should.

**💻 Run the image**

<details>
  <summary markdown='span'>💡 Hints</summary>

You should probably remove the interactivity mode and forget the `sh` command... Read below if you're stuck!
</details>

**😱 It is probably crashing with errors involving environment variables**

**❓ What is the difference between your local environment and image environment? 💬 Discuss with your buddy.**

<details>
  <summary markdown='span'>Answer</summary>

There is **no** `.env` in the image!!! The image has **no** access to the environment variables 😈
</details>

**💻 Using the `docker run --help` documentation, adapt the run command so the `.env` is sent to the image**

<details>
  <summary markdown='span'>🙈 Solution</summary>

The `--env-file` parameter to the rescue!

```bash
docker run -e PORT=8000 -p 8000:8000 --env-file path/to/.env $IMAGE
```
</details>

**❓ How would check the image runs correctly?**

<details>
  <summary markdown='span'>💡 Hints</summary>

The API should respond in your browser, go visit it!

Also you can check if the image runs with `docker ps` in a new terminal

</details>

It's Alive! 😱 🎉

**👀 Inspect your browser response 👉 [http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2](http://localhost:8000/predict?pickup_datetime=2013-07-06%2017:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2)**

**🛑 You can stop your container with `docker container stop <CONTAINER_ID>**

**👏 Congrats, you build your first ML predictive API inside a Docker container!**


</details>

<br>

# 4️⃣ Deploy the API 🌎

<details>
  <summary markdown='span'><strong>❓ Instructions </strong></summary>

Now we have built a **predictive API** Docker image that we are able to run on our local machine, we are 2 steps away from deploying:
- Push the **Docker image** to **Google Container Registry**
- Deploy the image on **Google Cloud Run** so that it gets instantiated into a **Docker container**

## Lightweight image

As a responsible ML Engineer, you know the size of an image is important when it comes to production. Depending the choice of the base image you used in your `Dockerfile`, the API image could be huge:
- `python:3.8.12-buster` 👉 `3.9GB`
- `python:3.8.12-slim`   👉 `3.1GB`
- `python:3.8.12-alpine` 👉 `3.1GB`

**❓ What is the heaviest requirement used by your API?**

<details>
  <summary markdown='span'>Answer</summary>

No doubt it is `tensorflow` with 1.1GB! You need to find a base image that is optimized for it.
</details>

**📝 Change your base image**

You may want to use a [tensorflow docker image](https://hub.docker.com/r/tensorflow/tensorflow) and don't forget to remove `tensorflow` from the `requirements.txt` on your container

- 💻 Build and run a lightweight local image of your API
- ✅ Make sure the API is still up and running
- 👀 Inspect the space saved with `docker images` and feel happy

## Push our prediction API image to Google Container Registry

**❓ What is the purpose of Google Container Registry ?**

<details>
  <summary markdown='span'>Answer</summary>

**Google Container Registry** is a service storing Docker images on the cloud with the purpose of allowing **Cloud Run** or **Kubernetes Engine** to serve them.

It is in a way similar to **GitHub** allowing you to store your git repositories in the cloud (except for the lack of a dedicated user interface and additional services such as `forks` and `pull requests`).

</details>

### Setup

First, let's make sure to enable [Google Container Registry API](https://console.cloud.google.com/flows/enableapi?apiid=containerregistry.googleapis.com&redirect=https://cloud.google.com/container-registry/docs/quickstart) for your project in GCP.

Once this is done, let's allow the `docker` command to push an image to GCP.

``` bash
gcloud auth configure-docker
```

### Build and push the image on GCR

Now we are going to build our image again. This should be pretty fast since Docker is pretty smart and is going to reuse all the building blocks used previously in order to build the prediction API image.

Add a `GCR_MULTI_REGION` variable to your project configuration and set it to `eu.gcr.io`.

``` bash
docker build -t $GCR_MULTI_REGION/$PROJECT/$IMAGE .
```

Again, let's make sure that our image runs correctly, so that we avoid spending the time on pushing an image that is not working to the cloud.

``` bash
docker run -e PORT=8000 -p 8000:8000 --env-file path/to/.env $GCR_MULTI_REGION/$PROJECT/$IMAGE
```
Visit [http://localhost:8000/](http://localhost:8000/) and check the API is running as expected.

We can now push our image to Google Container Registry.

``` bash
docker push $GCR_MULTI_REGION/$PROJECT/$IMAGE
```

The image should be visible in the GCP console [here](https://console.cloud.google.com/gcr/).

## Deploy the Container Registry image to Google Cloud Run

Add a `MEMORY` variable to your project configuration and set it to `2Gi`.

👉 This will allow your container to run with **2GB** of memory

**❓ How does Cloud Run know the value of the environment variables to pass to your container? 💬 Discuss with your buddy.**

<details>
  <summary markdown='span'>Answer</summary>

It does not. You need to provide a list of environment variables to your container when you deploy it 😈

</details>

**💻 Using the `gcloud run deploy --help` documentation, identify a parameter allowing to pass environment variables to your container on deployment**

<details>
  <summary markdown='span'>🙈 Solution</summary>

The `--env-vars-file` is the correct one!

```bash
gcloud run deploy --env-vars-file .env.yaml
```

Tough luck, the `--env-vars-file` parameter takes as input the name of a `yaml` file containing the list of environment variables to pass to the container.

</details>

**💻 Create a `.env.yaml` file containing the list of environment variables to pass to your container**

You can use the provided `.env.sample.yaml` file as a source for the syntax (do not forget to update the value of the parameters).

<details>
  <summary markdown='span'>🙈 Solution</summary>

Create a new `.env.yaml` file containing the values of your `.env` file in the `yaml` format:

``` yaml
DATASET_SIZE: 10k
VALIDATION_DATASET_SIZE: 10k
CHUNK_SIZE: "2000"
```

👉 All values should be strings

</details>

**❓ What is the purpose of Cloud Run?**

<details>
  <summary markdown='span'>Answer</summary>

Cloud Run will instantiate the image into a container and run the `CMD` instruction inside of the `Dockerfile` of the image. This last step will start the `uvicorn` server serving our **predictive API** to the world 🌍

</details>

Let's run one last command 🤞

``` bash
gcloud run deploy --image $GCR_MULTI_REGION/$PROJECT/$IMAGE --memory $MEMORY --region $REGION --env-vars-file .env.yaml
```

After confirmation, you should see a similar output indicating that the service is live 🎉

```bash
Service name (wagon-data-tpl-image):
Allow unauthenticated invocations to [wagon-data-tpl-image] (y/N)?  y

Deploying container to Cloud Run service [wagon-data-tpl-image] in project [le-wagon-data] region [europe-west1]
✓ Deploying new service... Done.
  ✓ Creating Revision... Revision deployment finished. Waiting for health check to begin.
  ✓ Routing traffic...
  ✓ Setting IAM Policy...
Done.
Service [wagon-data-tpl-image] revision [wagon-data-tpl-image-00001-kup] has been deployed and is serving 100 percent of traffic.
Service URL: https://wagon-data-tpl-image-xi54eseqrq-ew.a.run.app
```

Any developer in the world 🌍 is now able to browse to the deployed url and make a prediction using the API 🤖!

⚠️ Keep in mind that you pay for the service as long as it is up 💸

<details>
  <summary markdown='span'>Hint</summary>

You can look for the running instances using:

``` bash
gcloud compute instances list
```

You can shutdown your instance with:

``` bash
gcloud compute instances stop $INSTANCE
```

</details>

**👏 Congrats, you deployed your first ML predictive API!**

## Once you are done with Docker...

You may stop (or kill) the image...

``` bash
docker stop 152e5b79177b  # ⚠️ use the correct CONTAINER ID
docker kill 152e5b79177b  # ☢️ only if the image refuses to stop (did someone create an ∞ loop?)
```
Remember to stop the Docker daemon in order to free resources on your machine once you are done using it...

<details>
  <summary markdown='span'>MacOSX</summary>

Stop the `Docker.app` with **Quit Docker Desktop** in the menu bar.
</details>

<details>
  <summary markdown='span'>Windows WSL2/Ubuntu</summary>

Stop the Docker app.
</details>

</details>

<br>

# 5️⃣ OPTIONAL

<details>
  <summary markdown='span'><strong>❓ Instructions </strong></summary>

## 1) Create a /POST request to be able to return batch predictions

Let's look at our `/GET` route format

```bash
http://localhost:8000/predict?pickup_datetime=2014-07-06&19:18:00&pickup_longitude=-73.950655&pickup_latitude=40.783282&dropoff_longitude=-73.984365&dropoff_latitude=40.769802&passenger_count=2
```

🤯 How would you send a prediction request for 1000 rows at once?

The url query string (everything after `?` in the url above) is not adapted to send large volume of data.

### Welcome to `/POST` HTTP requests

- Your goal is to be able to send a batch of 1000 new predictions at once!
- Try to read more about post in [fast api docs](https://fastapi.tiangolo.com/tutorial/body/#request-body-path-query-parameters) and implement it on your package

## 2) Read about sending images 📸 via /POST requests to CNN models...

In anticipation to your demo-day, you might be wondering how to send unstructured data like images (or videos, or sounds etc...) to your deep-learning model in prod.


👉 Bookmark [Le Wagon - data-template](https://github.com/lewagon/data-templates) and try to understand & reproduce the project boilerplate called "[sending-images-streamlit-fastapi](https://github.com/lewagon/data-templates/tree/main/project-boilerplates/sending-images-streamlit-fastapi)"


</details>
