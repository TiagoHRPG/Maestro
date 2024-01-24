# Maestro
Maestro is a project that enables you to control Spotify media player using hand gestures. You can currently pause, play and skip songs by doing hand gestures on your webcam
## Technologies
I used **Python, Opencv, Mediapipe**

## Setup
1. Download or clone the repository

2. Change directory
```
cd Maestro
``` 

3. create a conda environment 
```
conda create -n maestro
```

4. Install requirements
```
pip install -r requirements.txt
```
5. Open Spotify

6. Run main script
```
python3 main.py
```

## Usage
When the script is executed, a window will pop-up showing your webcam. To control yout media player, simply raise your hand and do some gestures.

The gestures currently available are:

- ✋: raise LEFT hand       -> pause song
- ✋: raise RIGHT hand      -> play song
- ✌🏼: peace sign LEFT hand  -> previous song
- ✌🏼: peace sign RIGHT hand -> next song 

A gif below demonstrates the usage


![](https://github.com/TiagoHRPG/Maestro/blob/main/imgs/maestro_demo_gif.gif)

## License
MIT license
