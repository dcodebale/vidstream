from flask import Flask, Response, request, render_template_string
import time

app = Flask(__name__)

latest_frame = None


@app.route("/", methods=["GET"])
def index():
    return render_template_string("""
        <h1>Live Stream</h1>
        <img src="/stream">
    """)


@app.route("/upload", methods=["POST"])
def upload():
    global latest_frame
    latest_frame = request.data
    return "OK", 200


def generate_stream():
    global latest_frame
    while True:
        if latest_frame:
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" +
                   latest_frame + b"\r\n")
        time.sleep(0.1)  # ~10 fps


@app.route("/stream")
def stream():
    return Response(
        generate_stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
