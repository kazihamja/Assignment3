# Spot the Difference - Interactive Python Game

Welcome to the **Spot the Difference** game! This project is a student team collaboration built using Python, focusing on image processing and graphical user interface development.

## 🎮 About the Game
This application takes any standard image and dynamically generates five subtle differences on a modified version. Players must compare the "Original" and "Modified" images side-by-side and click on the areas where they spot a change.

### Key Features:
- **Dynamic Difference Generation**: Uses OpenCV to programmatically create unique differences every time an image is loaded.
- **Multiple Effect Types**: 
  - 🎨 **Color Shifting**: Subtle shifts in RGB channels.
  - 🌫️ **Gaussian Blur**: Localized blurring of image sections.
  - 💡 **Brightness Adjustments**: Changes in local lighting/intensity.
- **Game Mechanics**:
  - Score tracking for every found difference.
  - Miss counter (Game Over after 3 incorrect clicks).
  - "Reveal All" feature for when you're stuck.
- **Responsive UI**: Built with Tkinter, featuring automatic image scaling to fit your screen.

## 🛠️ Built With
- **Python 3**
- **Tkinter**: For the graphical user interface.
- **OpenCV (cv2)**: For advanced image manipulation and difference injection.
- **NumPy**: For efficient pixel-level array operations.
- **Pillow (PIL)**: For image format conversion and handling within Tkinter.

## 📂 Project Structure
There are two ways to run the project:

### 1. Modular Version (Recommended for Development)
Located in the `TeamProject/` folder. This version follows OOP best practices by separating concerns:
- `TeamProject/main.py`: The entry point and UI controller.
- `TeamProject/image_lib.py`: Core image processing logic.
- `TeamProject/effects.py`: Visual change implementations.
- `TeamProject/logic.py`: Game state management.

### 2. Single-File Version (For Portability)
- `spot_the_difference.py`: A consolidated version containing all logic in one file.

## 🚀 Getting Started

### Prerequisites
Ensure you have Python installed, then install the required dependencies:

```bash
pip install opencv-python numpy pillow
```

### Running the Game
To run the modular version:
```bash
python TeamProject/main.py
```

To run the single-file version:
```bash
python spot_the_difference.py
```


## 👥 Team Contributions
This project was developed as a collaborative effort:
- **UI/UX & Integration**: Person 1
- **Image Processing Architecture**: Person 2
- **Visual Effects Implementation**: Person 3
- **Game Logic & State Management**: Person 4

## 📜 License
This project is for educational purposes as part of a university assignment.
