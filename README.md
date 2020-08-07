# ageage-ec2

when CodePipeline execution started, start instances if that is not running 

## requirements

* SAM CLI
* Docker

## build && deploy

```bash
sam build -u

sam deploy
```

## invoke

```bash
sam local invoke --event events/event.json
```
