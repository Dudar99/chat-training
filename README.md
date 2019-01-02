# Chat-training

This application allow you to send and recieve messages using kafka brokers.
Messages  store to databases (Postgres or Cassandra)

## Getting Started

```
git clone https://github.com/Dudar99/chat-training.git
```

### Prerequisites

You need to build application with docker and docker-compose utils so install it and run:

```
cd chat-training
sudo docker-compose up --build
```

### Installing

Wait until docker install all dependencies(it may take 5 min)

Then docker will run all containers

Wait until consumer app give you message like this :"connection with Kafka broker successfully established"


## Endpoints
```
send message - http://127.0.0.1:5000/
check rowcount - http://127.0.0.1:5001/count
check offset - http://127.0.0.1:5001/offset
```

## Running the tests

TODO
### Break down into end to end tests


### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* docker
* docker-compose

## Authors

* **Yurii Dudar** - *Initial work* 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used

