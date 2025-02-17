# mse_auto_checking_slides_yastrebkov

This project uses simple natural language processing methods to analyze document structure. The application should check how clear document's base goals and objectives were uncovered. It can check presentation files (ppt, pptx, odp, odpx) with a number of [criterias](http://se.moevm.info/doku.php/diplomants:start:slides_checklist_etu).

More information can be found [here](http://se.moevm.info/doku.php/courses:mse:projects_2020#r_d_4_%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F_%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0_%D0%B4%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%D0%BD%D1%8B%D1%85_%D0%BF%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B9).

### Team members

* Curator: [Veronika Veroha](https://github.com/veronav), email: veronav111@mail.ru
* Leader: [Anton Yastrebkov](https://github.com/AntonYastrebkov), email: anton.yastrebkoff@gmail.com
* Team members:
  * [Matrosov Denis]()
  * [Meshkov Maksim](https://github.com/Heliconter), email: maaaxme@gmail.com
  * [Pavel Poryvai](https://github.com/Pavel377dq)
  
### Activity tracker

Team uses GitHub Projects for activity tracking. The activity board can be found [here](https://github.com/moevm/mse_auto_checking_slides_yastrebkov/projects/1).

#### Iterations:

- Iteration 1: base app with simple UI ([issues](https://github.com/moevm/mse_auto_checking_slides_yastrebkov/milestone/1))
- Iteration 2: improved UI, user registration, DB connection, investigating libraries to wirk with presentations ([issues](https://github.com/moevm/mse_auto_checking_slides_yastrebkov/milestone/2))
- Iteration 3: implementation of simple presentation checks, implement customization of checks ([issues](https://github.com/moevm/mse_auto_checking_slides_yastrebkov/milestone/3))
- Iteration 4: implementation of all checks, Docker integration ([issues](https://github.com/moevm/mse_auto_checking_slides_yastrebkov/milestone/4))

## Launch

### Launch with Docker Compose

To launch project you need Docker and Docker Compose installed. 
Instructions for installation can be found on the official site ([Docker](https://docs.docker.com/engine/install/ubuntu/), [Docker Compose](https://docs.docker.com/compose/install/))

0. Make sure your Docker is ready to launch. It can be done with command:

```shell
sudo docker run hello-world
```

1. Clone repository to your local computer and navigate to project folder:

```shell
git clone https://github.com/moevm/mse_auto_checking_slides_yastrebkov.git
cd mse_auto_checking_slides_yastrebkov
```

Checkout to `master-local` branch:

```shell
git checkout master-local
```

2. Run docker-compose:

```shell
sudo docker-compose -up
```

Or, if you want to run it in a silent mode:

```shell
sudo docker-compose up -d
```

If everything worked well, you will see launching container. 
Make a cup of coffee or tea, first launch needs a couple of minutes to download and build images.

3. Navigate to [`http://localhost:80`](http://localhost:80) in your browser and enjoy.

4. To stop containers, press `Ctrl+C`. If you launched docker-compose with `-d` flag, than use command:

```shell
sudo docker-compose down
```

**NB:** You can use docker commands without sudo, instruction can be found [here](https://docs.docker.com/engine/install/linux-postinstall/).

If you want to delete all created containers, volumes, images, use command (be careful, it would delete *all* your docker-related data):

```shell
sudo docker system prune --volumes
```

### Deprecated launch

To launch project you need Python 3 installed on your computer. To install Python, follow [official site's](https://wiki.python.org/moin/BeginnersGuide/Download) instructions. This project assumed to work on Ubuntu 18.04 or later. Stable launching on other operation systems is not guaranteed.

0. Clone repository on local computer and go to project directory:

```shell script
git clone https://github.com/moevm/mse_auto_checking_slides_yastrebkov.git
cd mse_auto_checking_slides_yastrebkov/app
```

To launch the application, you need MongoDB installed and running on default host and ort. Instructions for installing and launching MongoDB can be found on [official site](https://docs.mongodb.com/manual/installation/).

1. Create and activate virtual environment for the project:

```shell script
python -m venv env --system-site-packages
source ./env/bin/activate
```

If your default Python is Python 2, use `python3`.

2. Install dependencies:

```shell script
pip install -r requirements.txt
```

**NB:** run this command if dependencies were updated since last launch. You can run this command before every launch, if all dependencies were already installed in your virtual environment, it will do nothing.

3. Run application:

```shell script
python server.py --host 127.0.0.1 --port 5000
```

Values for `host` and `port` arguments can be different, but it is strongly recommended to use default values: `127.0.0.1` and `5000` respectively. If you don't pass arguments, default values `0.0.0.0` and `80` will be used. This configuration is suitable for service environment and probably won't run on your local machine.

4. Navigate to localhost:5000 or 127.0.0.1:5000 in your browser and enjoy.

