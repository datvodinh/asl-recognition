# Sign Language Detection

![Alt text](img/image.png)

## Result

![Alt text](img/result.png)

## Clone

```bash
git clone https://github.com/datvodinh/sign-language-detection.git
cd sign-language-detection # IF NOT ALREADY IN
```

## Setup, Build Package and download Checkpoint, Dataset and Demo

```bash
source ./scripts/setup.sh
```

## Train

```bash
python -m dl_project.train --model resnet --batch_size 64
```

### Train all

```bash
python -m dl_project.train --model all --batch_size 64
```

### Train Demo

```bash
python -m dl_project.train --model resnet --batch_size 64 --max_epochs 10 --folder generate --name demo
```

### Run Demo

```bash
python app.py
```

## Help

```bash
python -m dl_project.train -h
```
