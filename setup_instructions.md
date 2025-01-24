# Setup Instructions

## Setting up a Virtual Environment

1. **Navigate to your project directory:**

2. **Create a virtual environment:**
    ```sh
    python3 -m venv venv
    ```

3. **Activate the virtual environment:**
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```

4. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Running the Files

1. **Ensure the virtual environment is activated:**
    ```sh
    source venv/bin/activate  # macOS/Linux
    .\venv\Scripts\activate  # Windows
    ```

2. **Run the desired Python file:**
    ```sh
    python <your_script.py>
    ```

3. **Run the tests using unittest:**
    ```sh
    python -m unittest discover
    ```