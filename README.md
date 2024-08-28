# Book Owl

**Book Owl** is a user-friendly web application that converts PDF documents into audio files. It includes user authentication and integrates with Flutterwave for secure payments.

## Features

- PDF to Audio Conversion
- User Authentication (Sign-Up and Login)
- flutterwave Integration for Payments
- Responsive Design

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Danielfavour6002/BookOwl/.git
    cd BookOwl
    ```

2. **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Set up the database:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

4. **Run the application:**
    ```bash
    flask run or py app.py
    ```

5. **Open your web browser and visit:**
    ```
    http://127.0.0.1:5000
    ```

## Usage

1. **'/'**: Create a new account or log in with an existing one.
2. **'/home'**: Select a PDF file to convert to audio.
3. **'/Payment'**: for secure payments.
4. **'/Download<filename>'**: Download the converted MP3 file.

## Configuration

- Ensure you set a secure `SECRET_KEY` for session management. This can be set in your environment variables or directly in the Flask configuration file.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b develop-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin develop-branch`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For inquiries or suggestions, please contact [feivodanny.06@gmail.com]
